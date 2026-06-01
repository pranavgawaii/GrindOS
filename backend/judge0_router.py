from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import base64
import re
import os
import json
import sqlite3

router = APIRouter()

class CodeRequest(BaseModel):
    problem_id: str
    language: str
    source_code: str
    testcases: list = None

JUDGE0_LANG_IDS = {
    "python": 100,      # Python (3.12.5)
    "cpp": 105,         # C++ (GCC 14.1.0)
    "java": 91,         # Java (JDK 17.0.6)
    "javascript": 102   # JavaScript (Node.js 22.08.0)
}

PROBLEMS_TEST_CASES = {
    "#1": {
        "method_name": "twoSum",
        "public": [
            {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"inputs": [[3, 2, 4], 6], "expected": [1, 2]}
        ],
        "hidden": [
            {"inputs": [[3, 3], 6], "expected": [0, 1]},
            {"inputs": [[2, 5, 5, 11], 10], "expected": [1, 2]}
        ]
    },
    "#217": {
        "method_name": "containsDuplicate",
        "public": [
            {"inputs": [[1, 2, 3, 1]], "expected": True},
            {"inputs": [[1, 2, 3, 4]], "expected": False}
        ],
        "hidden": [
            {"inputs": [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], "expected": True},
            {"inputs": [[3]], "expected": False}
        ]
    },
    "#242": {
        "method_name": "isAnagram",
        "public": [
            {"inputs": ["anagram", "nagaram"], "expected": True},
            {"inputs": ["rat", "car"], "expected": False}
        ],
        "hidden": [
            {"inputs": ["a", "ab"], "expected": False},
            {"inputs": ["awesome", "someawe"], "expected": True}
        ]
    },
    "#20": {
        "method_name": "isValid",
        "public": [
            {"inputs": ["()"], "expected": True},
            {"inputs": ["()[]{}"], "expected": True}
        ],
        "hidden": [
            {"inputs": ["(]"], "expected": False},
            {"inputs": ["(["], "expected": False}
        ]
    },
    "#704": {
        "method_name": "search",
        "public": [
            {"inputs": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
            {"inputs": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1}
        ],
        "hidden": [
            {"inputs": [[5], 5], "expected": 0},
            {"inputs": [[2, 5], 5], "expected": 1}
        ]
    }
}

def clean_user_code_python(code: str) -> str:
    lines = []
    for line in code.splitlines():
        if line.strip().startswith("# Test") or line.strip().startswith("sol = Solution()") or line.strip().startswith("print(sol."):
            break
        lines.append(line)
    return "\n".join(lines)

def clean_user_code_js(code: str) -> str:
    lines = []
    for line in code.splitlines():
        if line.strip().startswith("// Test") or line.strip().startswith("console.log("):
            break
        lines.append(line)
    return "\n".join(lines)

def clean_user_code_cpp(code: str) -> str:
    parts = re.split(r'int\s+main\s*\(', code)
    return parts[0]

def clean_user_code_java(code: str) -> str:
    parts = re.split(r'(public\s+)?class\s+Main', code)
    return parts[0]

def wrap_code(problem_id: str, language: str, source_code: str, testcases: list) -> str:
    if problem_id not in PROBLEMS_TEST_CASES:
        return source_code
    
    prob = PROBLEMS_TEST_CASES[problem_id]
    method_name = prob["method_name"]
    
    if language == "python":
        clean_code = clean_user_code_python(source_code)
        driver = f"""
# TEST RUNNER DRIVER
import json
_tc = {json.dumps(testcases)}
_results = []
for _case in _tc:
    try:
        _sol = Solution()
        _res = _sol.{method_name}(*_case["inputs"])
        _expected = _case["expected"]
        if isinstance(_res, list) and isinstance(_expected, list):
            _passed = sorted(_res) == sorted(_expected)
        else:
            _passed = _res == _expected
        _results.append({{"passed": _passed, "actual": _res, "expected": _expected, "inputs": _case["inputs"]}})
    except Exception as _e:
        _results.append({{"passed": False, "error": str(_e), "inputs": _case["inputs"]}})
print("---TEST_RESULTS_JSON---")
print(json.dumps(_results))
"""
        return clean_code + "\n" + driver
        
    elif language == "javascript":
        clean_code = clean_user_code_js(source_code)
        driver = f"""
// TEST RUNNER DRIVER
const _tc = {json.dumps(testcases)};
const _results = [];
for (const _case of _tc) {{
    try {{
        let _res;
        if (typeof Solution !== 'undefined') {{
            const _sol = new Solution();
            _res = _sol.{method_name}(..._case.inputs);
        }} else {{
            _res = {method_name}(..._case.inputs);
        }}
        const _expected = _case.expected;
        let _passed = false;
        if (Array.isArray(_res) && Array.isArray(_expected)) {{
            _passed = JSON.stringify(_res.slice().sort()) === JSON.stringify(_expected.slice().sort());
        }} else {{
            _passed = _res === _expected;
        }}
        _results.push({{passed: _passed, actual: _res, expected: _expected, inputs: _case.inputs}});
    }} catch (_e) {{
        _results.push({{passed: false, error: _e.message, inputs: _case.inputs}});
    }}
}}
console.log("---TEST_RESULTS_JSON---");
console.log(JSON.stringify(_results));
"""
        return clean_code + "\n" + driver
        
    elif language == "cpp":
        clean_code = clean_user_code_cpp(source_code)
        cases_cpp = []
        for case in testcases:
            inputs = case["inputs"]
            expected = case["expected"]
            
            if problem_id == "#1":
                nums_str = ", ".join(map(str, inputs[0]))
                target = inputs[1]
                exp0, exp1 = expected[0], expected[1]
                case_code = f"""
{{
    vector<int> nums = {{{nums_str}}};
    int target = {target};
    vector<int> res = sol.twoSum(nums, target);
    bool passed = false;
    if (res.size() == 2) {{
        if ((res[0] == {exp0} && res[1] == {exp1}) || (res[0] == {exp1} && res[1] == {exp0})) {{
            passed = true;
        }}
    }}
    cout << "{{\\"passed\\":" << (passed ? "true" : "false") << ",\\"actual\\":[" << (res.size() > 0 ? to_string(res[0]) : "") << "," << (res.size() > 1 ? to_string(res[1]) : "") << "],\\"expected\\":[{exp0},{exp1}]}}";
}}"""
            elif problem_id == "#217":
                nums_str = ", ".join(map(str, inputs[0]))
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    vector<int> nums = {{{nums_str}}};
    bool res = sol.containsDuplicate(nums);
    bool passed = (res == {exp_str});
    cout << "{{\\"passed\\":" << (passed ? "true" : "false") << ",\\"actual\\":" << (res ? "true" : "false") << ",\\"expected\\":" << ({exp_str} ? "true" : "false") << "}}";
}}"""
            elif problem_id == "#242":
                s, t = inputs[0], inputs[1]
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    string s = "{s}";
    string t = "{t}";
    bool res = sol.isAnagram(s, t);
    bool passed = (res == {exp_str});
    cout << "{{\\"passed\\":" << (passed ? "true" : "false") << ",\\"actual\\":" << (res ? "true" : "false") << ",\\"expected\\":" << ({exp_str} ? "true" : "false") << "}}";
}}"""
            elif problem_id == "#20":
                s = inputs[0]
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    string s = "{s}";
    bool res = sol.isValid(s);
    bool passed = (res == {exp_str});
    cout << "{{\\"passed\\":" << (passed ? "true" : "false") << ",\\"actual\\":" << (res ? "true" : "false") << ",\\"expected\\":" << ({exp_str} ? "true" : "false") << "}}";
}}"""
            elif problem_id == "#704":
                nums_str = ", ".join(map(str, inputs[0]))
                target = inputs[1]
                exp_val = expected
                case_code = f"""
{{
    vector<int> nums = {{{nums_str}}};
    int target = {target};
    int res = sol.search(nums, target);
    bool passed = (res == {exp_val});
    cout << "{{\\"passed\\":" << (passed ? "true" : "false") << ",\\"actual\\":" << to_string(res) << ",\\"expected\\":" << to_string({exp_val}) << "}}";
}}"""
            else:
                case_code = ""
            cases_cpp.append(case_code)
            
        joined_cases = '\ncout << ",";\n'.join(cases_cpp)
        driver = f"""
int main() {{
    Solution sol;
    cout << "---TEST_RESULTS_JSON---" << endl;
    cout << "[";
    {joined_cases}
    cout << "]" << endl;
    return 0;
}}
"""
        return clean_code + "\n" + driver

    elif language == "java":
        clean_code = clean_user_code_java(source_code)
        cases_java = []
        for case in testcases:
            inputs = case["inputs"]
            expected = case["expected"]
            
            if problem_id == "#1":
                nums_str = ", ".join(map(str, inputs[0]))
                target = inputs[1]
                exp0, exp1 = expected[0], expected[1]
                case_code = f"""
{{
    int[] nums = new int[]{{{nums_str}}};
    int target = {target};
    int[] res = sol.twoSum(nums, target);
    boolean passed = false;
    if (res != null && res.length == 2) {{
        if ((res[0] == {exp0} && res[1] == {exp1}) || (res[0] == {exp1} && res[1] == {exp0})) {{
            passed = true;
        }}
    }}
    System.out.print("{{\\"passed\\":" + passed + ",\\"actual\\":[" + (res != null && res.length > 0 ? res[0] : "") + "," + (res != null && res.length > 1 ? res[1] : "") + "],\\"expected\\":[{exp0},{exp1}]}}");
}}"""
            elif problem_id == "#217":
                nums_str = ", ".join(map(str, inputs[0]))
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    int[] nums = new int[]{{{nums_str}}};
    boolean res = sol.containsDuplicate(nums);
    boolean passed = (res == {exp_str});
    System.out.print("{{\\"passed\\":" + passed + ",\\"actual\\":" + res + ",\\"expected\\":" + {exp_str} + "}}");
}}"""
            elif problem_id == "#242":
                s, t = inputs[0], inputs[1]
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    String s = "{s}";
    String t = "{t}";
    boolean res = sol.isAnagram(s, t);
    boolean passed = (res == {exp_str});
    System.out.print("{{\\"passed\\":" + passed + ",\\"actual\\":" + res + ",\\"expected\\":" + {exp_str} + "}}");
}}"""
            elif problem_id == "#20":
                s = inputs[0]
                exp_str = "true" if expected else "false"
                case_code = f"""
{{
    String s = "{s}";
    boolean res = sol.isValid(s);
    boolean passed = (res == {exp_str});
    System.out.print("{{\\"passed\\":" + passed + ",\\"actual\\":" + res + ",\\"expected\\":" + {exp_str} + "}}");
}}"""
            elif problem_id == "#704":
                nums_str = ", ".join(map(str, inputs[0]))
                target = inputs[1]
                exp_val = expected
                case_code = f"""
{{
    int[] nums = new int[]{{{nums_str}}};
    int target = {target};
    int res = sol.search(nums, target);
    boolean passed = (res == {exp_val});
    System.out.print("{{\\"passed\\":" + passed + ",\\"actual\\":" + res + ",\\"expected\\":" + {exp_val} + "}}");
}}"""
            else:
                case_code = ""
            cases_java.append(case_code)
            
        joined_cases = '\nSystem.out.print(",");\n'.join(cases_java)
        driver = f"""
public class Main {{
    public static void main(String[] args) {{
        Solution sol = new Solution();
        System.out.println("---TEST_RESULTS_JSON---");
        System.out.print("[");
        {joined_cases}
        System.out.println("]");
    }}
}}
"""
        return clean_code + "\n" + driver
    
    return source_code

def decode_base64(s: str) -> str:
    if not s:
        return ""
    try:
        return base64.b64decode(s.encode('utf-8')).decode('utf-8')
    except Exception:
        return s

def parse_driver_results(stdout: str) -> tuple[list, str]:
    if "---TEST_RESULTS_JSON---" not in stdout:
        return None, stdout
        
    parts = stdout.split("---TEST_RESULTS_JSON---")
    output_before = parts[0].strip()
    json_part = parts[1].strip()
    
    try:
        results = json.loads(json_part)
        return results, output_before
    except Exception:
        return None, stdout

async def execute_on_judge0(source_code: str, language: str) -> dict:
    url = os.getenv("JUDGE0_API_URL", "https://judge0-ce.p.rapidapi.com")
    api_key = os.getenv("JUDGE0_API_KEY", "")
    is_rapidapi = os.getenv("JUDGE0_IS_RAPIDAPI", "true").lower() == "true"
    
    if url.endswith("/"):
        url = url[:-1]
        
    endpoint = f"{url}/submissions?wait=true&base64_encoded=true"
    lang_id = JUDGE0_LANG_IDS.get(language, 71)
    
    encoded_code = base64.b64encode(source_code.encode("utf-8")).decode("utf-8")
    
    payload = {
        "source_code": encoded_code,
        "language_id": lang_id
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if api_key:
        if is_rapidapi:
            headers["X-RapidAPI-Key"] = api_key
            headers["X-RapidAPI-Host"] = url.replace("https://", "").replace("http://", "").split("/")[0]
        else:
            headers["X-Auth-Token"] = api_key
            
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(endpoint, json=payload, headers=headers)
        
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=500, detail=f"Judge0 sandbox error: {response.text}")
        
    res_data = response.json()
    
    stdout = decode_base64(res_data.get("stdout"))
    stderr = decode_base64(res_data.get("stderr"))
    compile_output = decode_base64(res_data.get("compile_output"))
    
    status = res_data.get("status", {})
    status_id = status.get("id")
    status_desc = status.get("description")
    
    runtime = res_data.get("time")
    memory = res_data.get("memory")
    
    return {
        "stdout": stdout,
        "stderr": stderr,
        "compile_output": compile_output,
        "status_id": status_id,
        "status_desc": status_desc,
        "runtime": runtime,
        "memory": memory
    }

def run_sql_query(problem_id: str, query: str) -> dict:
    SQL_DB_SETUP = {
        "#1757": {
            "setup": """
                CREATE TABLE Products (product_id INT PRIMARY KEY, low_fats VARCHAR(1), recyclable VARCHAR(1));
                INSERT INTO Products VALUES (0, 'Y', 'N'), (1, 'Y', 'Y'), (2, 'N', 'Y'), (3, 'Y', 'Y'), (4, 'N', 'N');
            """,
            "solution": "SELECT product_id FROM Products WHERE low_fats = 'Y' AND recyclable = 'Y';"
        },
        "#584": {
            "setup": """
                CREATE TABLE Customer (id INT PRIMARY KEY, name VARCHAR(25), referee_id INT);
                INSERT INTO Customer VALUES (1, 'Will', NULL), (2, 'Jane', NULL), (3, 'Alex', 2), (4, 'Bill', NULL), (5, 'Zack', 1), (6, 'Mark', 2);
            """,
            "solution": "SELECT name FROM Customer WHERE referee_id != 2 OR referee_id IS NULL;"
        },
        "#595": {
            "setup": """
                CREATE TABLE World (name VARCHAR(50) PRIMARY KEY, continent VARCHAR(50), area INT, population INT, gdp INT);
                INSERT INTO World VALUES 
                ('Afghanistan', 'Asia', 652230, 25500100, 20343000000),
                ('Albania', 'Europe', 28748, 2831741, 12901000000),
                ('Algeria', 'Africa', 2381741, 37100000, 188681000000),
                ('Andorra', 'Europe', 468, 78115, 3712000000),
                ('Angola', 'Africa', 1246700, 20609294, 100990000000);
            """,
            "solution": "SELECT name, population, area FROM World WHERE area >= 3000000 OR population >= 25000000;"
        }
    }
    
    if problem_id not in SQL_DB_SETUP:
        return {
            "status": "runtime_error",
            "error": f"SQL Problem ID {problem_id} not registered in sandbox schemas.",
            "runtime": "0",
            "memory": 0
        }
        
    setup_script = SQL_DB_SETUP[problem_id]["setup"]
    solution_query = SQL_DB_SETUP[problem_id]["solution"]
    
    conn = sqlite3.connect(":memory:")
    try:
        cursor = conn.cursor()
        cursor.executescript(setup_script)
        
        try:
            cursor.execute(query)
            user_cols = [desc[0] for desc in cursor.description] if cursor.description else []
            user_rows = cursor.fetchall()
        except Exception as e:
            return {
                "status": "compile_error",
                "error": str(e),
                "runtime": "0.01",
                "memory": 120
            }
            
        cursor.execute(solution_query)
        sol_cols = [desc[0] for desc in cursor.description] if cursor.description else []
        sol_rows = cursor.fetchall()
        
        passed = False
        if len(user_cols) == len(sol_cols):
            user_cols_lower = [c.lower() for c in user_cols]
            sol_cols_lower = [c.lower() for c in sol_cols]
            if user_cols_lower == sol_cols_lower:
                if sorted(user_rows) == sorted(sol_rows):
                    passed = True
                
        stdout_rows = [f"| {' | '.join(user_cols)} |"]
        stdout_rows.append(f"| {' | '.join(['---'] * len(user_cols))} |")
        for row in user_rows:
            stdout_rows.append(f"| {' | '.join(str(val) if val is not None else 'NULL' for val in row)} |")
        stdout = "\n".join(stdout_rows)
        
        actual_str = f"Columns: {', '.join(user_cols)}\nRows count: {len(user_rows)}"
        expected_str = f"Columns: {', '.join(sol_cols)}\nRows count: {len(sol_rows)}"
        
        return {
            "status": "success",
            "testcases": [
                {
                    "passed": passed,
                    "actual": actual_str,
                    "expected": expected_str,
                    "inputs": [query]
                }
            ],
            "stdout": stdout,
            "stderr": "",
            "runtime": "0.01",
            "memory": 120
        }
    finally:
        conn.close()

@router.post("/run-code")
async def run_code(req: CodeRequest):
    if req.language.lower() == 'sql':
        return run_sql_query(req.problem_id, req.source_code)
    testcases = req.testcases
    if not testcases and req.problem_id in PROBLEMS_TEST_CASES:
        testcases = PROBLEMS_TEST_CASES[req.problem_id]["public"]
        
    wrapped = wrap_code(req.problem_id, req.language, req.source_code, testcases)
    
    try:
        res = await execute_on_judge0(wrapped, req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if res["status_id"] == 6:
        return {
            "status": "compile_error",
            "error": res["compile_output"] or res["stderr"],
            "runtime": res["runtime"],
            "memory": res["memory"]
        }
    elif res["status_id"] not in [3, 4]:
        return {
            "status": "runtime_error",
            "error": res["stderr"] or res["status_desc"],
            "runtime": res["runtime"],
            "memory": res["memory"]
        }
        
    if req.problem_id in PROBLEMS_TEST_CASES:
        results, clean_stdout = parse_driver_results(res["stdout"])
        if results is not None:
            return {
                "status": "success",
                "testcases": results,
                "stdout": clean_stdout,
                "stderr": res["stderr"],
                "runtime": res["runtime"],
                "memory": res["memory"]
            }
            
    return {
        "status": "success",
        "stdout": res["stdout"],
        "stderr": res["stderr"],
        "runtime": res["runtime"],
        "memory": res["memory"],
        "is_script": True
    }

@router.post("/submit-code")
async def submit_code(req: CodeRequest):
    if req.language.lower() == 'sql':
        res = run_sql_query(req.problem_id, req.source_code)
        if res["status"] == "success":
            all_passed = all(tc.get("passed", False) for tc in res.get("testcases", []))
            res["status"] = "accepted" if all_passed else "wrong_answer"
        return res
    testcases = []
    if req.problem_id in PROBLEMS_TEST_CASES:
        testcases = PROBLEMS_TEST_CASES[req.problem_id]["public"] + PROBLEMS_TEST_CASES[req.problem_id]["hidden"]
        
    wrapped = wrap_code(req.problem_id, req.language, req.source_code, testcases)
    
    try:
        res = await execute_on_judge0(wrapped, req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if res["status_id"] == 6:
        return {
            "status": "compile_error",
            "error": res["compile_output"] or res["stderr"],
            "runtime": res["runtime"],
            "memory": res["memory"]
        }
    elif res["status_id"] not in [3, 4]:
        return {
            "status": "runtime_error",
            "error": res["stderr"] or res["status_desc"],
            "runtime": res["runtime"],
            "memory": res["memory"]
        }
        
    if req.problem_id in PROBLEMS_TEST_CASES:
        results, clean_stdout = parse_driver_results(res["stdout"])
        if results is not None:
            all_passed = all(tc.get("passed", False) for tc in results)
            return {
                "status": "accepted" if all_passed else "wrong_answer",
                "testcases": results,
                "stdout": clean_stdout,
                "stderr": res["stderr"],
                "runtime": res["runtime"],
                "memory": res["memory"]
            }
            
    return {
        "status": "accepted" if res["status_id"] == 3 else "wrong_answer",
        "stdout": res["stdout"],
        "stderr": res["stderr"],
        "runtime": res["runtime"],
        "memory": res["memory"],
        "is_script": True
    }
