const DSA_PROBLEMS_DB = {
  "#1": {
    name: "Two Sum",
    difficulty: "Easy",
    method_name: "twoSum",
    tags: ["Arrays", "Hash Table", "Two Pointers"],
    constraints: [
      "2 <= nums.length <= 10^4",
      "-10^9 <= nums[i] <= 10^9",
      "-10^9 <= target <= 10^9",
      "Only one valid answer exists."
    ],
    hints: [
      "A brute force approach would search for all pairs, which takes O(N^2) time.",
      "Can we optimize this by keeping track of the target complement (target - nums[i]) as we iterate?",
      "Use a hash map to map each value to its index. This allows O(1) lookups."
    ],
    testcases: [
      { inputs: [[2, 7, 11, 15], 9], expected: [0, 1] },
      { inputs: [[3, 2, 4], 6], expected: [1, 2] }
    ],
    hidden_testcases: [
      { inputs: [[3, 3], 6], expected: [0, 1] },
      { inputs: [[2, 5, 5, 11], 10], expected: [1, 2] }
    ],
    desc: `Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.<br><br>
    You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.<br><br>
    You can return the answer in any order.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].</pre>`,
    stubs: {
      python: `class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # Write your code here
        pass
`,
      cpp: `#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Write your code here
        return {};
    }
};
`,
      java: `import java.util.Arrays;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[0];
    }
}
`,
      javascript: `var twoSum = function(nums, target) {
    // Write your code here
    
};
`,
      c: `#include <stdio.h>
#include <stdlib.h>

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // Write your code here
    *returnSize = 2;
    int* res = (int*)malloc(2 * sizeof(int));
    return res;
}
`
    }
  },
  "#217": {
    name: "Contains Duplicate",
    difficulty: "Easy",
    method_name: "containsDuplicate",
    tags: ["Arrays", "Hash Table", "Sorting"],
    constraints: [
      "1 <= nums.length <= 10^5",
      "-10^9 <= nums[i] <= 10^9"
    ],
    hints: [
      "We can sort the array and compare adjacent elements. Sorting takes O(N log N) time.",
      "Can we do it in O(N) time? We can use a hash set to store elements we've seen so far."
    ],
    testcases: [
      { inputs: [[1, 2, 3, 1]], expected: true },
      { inputs: [[1, 2, 3, 4]], expected: false }
    ],
    hidden_testcases: [
      { inputs: [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], expected: true },
      { inputs: [[3]], expected: false }
    ],
    desc: `Given an integer array <code>nums</code>, return <code>true</code> if any value appears <strong>at least twice</strong> in the array, and return <code>false</code> if every element is distinct.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: nums = [1,2,3,1]
Output: true</pre>`,
    stubs: {
      python: `class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        # Write your code here
        pass
`,
      cpp: `#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        // Write your code here
        return false;
    }
};
`,
      java: `import java.util.HashSet;

class Solution {
    public boolean containsDuplicate(int[] nums) {
        // Write your code here
        return false;
    }
}
`,
      javascript: `var containsDuplicate = function(nums) {
    // Write your code here
    
};
`,
      c: `#include <stdio.h>
#include <stdbool.h>

bool containsDuplicate(int* nums, int numsSize) {
    // Write your code here
    return false;
}
`
    }
  },
  "#242": {
    name: "Valid Anagram",
    difficulty: "Easy",
    method_name: "isAnagram",
    tags: ["String", "Hash Table", "Sorting"],
    constraints: [
      "1 <= s.length, t.length <= 5 * 10^4",
      "s and t consist of lowercase English letters."
    ],
    hints: [
      "An anagram is formed by rearranging letters. Sorting both strings would result in identical strings if they are anagrams.",
      "Can we count occurrences? A frequency map of size 26 (for lowercase English letters) can keep count of character occurrences in O(N) time."
    ],
    testcases: [
      { inputs: ["anagram", "nagaram"], expected: true },
      { inputs: ["rat", "car"], expected: false }
    ],
    hidden_testcases: [
      { inputs: ["a", "ab"], expected: false },
      { inputs: ["awesome", "someawe"], expected: true }
    ],
    desc: `Given two strings <code>s</code> and <code>t</code>, return <code>true</code> <em>if <code>t</code> is an anagram of <code>s</code>, and <code>false</code> otherwise</em>.<br><br>
    An <strong>Anagram</strong> is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: s = "anagram", t = "nagaram"
Output: true</pre>`,
    stubs: {
      python: `class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Write your code here
        pass
`,
      cpp: `#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    bool isAnagram(string s, string t) {
        // Write your code here
        return false;
    }
};
`,
      java: `import java.util.Arrays;

class Solution {
    public boolean isAnagram(String s, String t) {
        // Write your code here
        return false;
    }
}
`,
      javascript: `var isAnagram = function(s, t) {
    // Write your code here
    
};
`,
      c: `#include <stdio.h>
#include <stdbool.h>
#include <string.h>

bool isAnagram(char* s, char* t) {
    // Write your code here
    return false;
}
`
    }
  },
  "#20": {
    name: "Valid Parentheses",
    difficulty: "Easy",
    method_name: "isValid",
    tags: ["Stack", "String"],
    constraints: [
      "1 <= s.length <= 10^4",
      "s consists of parentheses only: '()[]{}'."
    ],
    hints: [
      "An open bracket must close in the correct order. This suggests a Last-In-First-Out data structure like a Stack.",
      "Push open brackets to the stack. When you encounter a close bracket, verify if the top of the stack matches its opening pair.",
      "At the end, check if the stack is completely empty. If not, the parentheses are invalid."
    ],
    testcases: [
      { inputs: ["()"], expected: true },
      { inputs: ["()[]{}"], expected: true }
    ],
    hidden_testcases: [
      { inputs: ["(]"], expected: false },
      { inputs: ["(["], expected: false }
    ],
    desc: `Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.<br><br>
    An input string is valid if:<br>
    1. Open brackets must be closed by the same type of brackets.<br>
    2. Open brackets must be closed in the correct order.<br>
    3. Every close bracket has a corresponding open bracket of the same type.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: s = "()"
Output: true</pre>`,
    stubs: {
      python: `class Solution:
    def isValid(self, s: str) -> bool:
        # Write your code here
        pass
`,
      cpp: `#include <iostream>
#include <stack>
#include <string>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        // Write your code here
        return false;
    }
};
`,
      java: `import java.util.Stack;

class Solution {
    public boolean isValid(String s) {
        // Write your code here
        return false;
    }
}
`,
      javascript: `var isValid = function(s) {
    // Write your code here
    
};
`,
      c: `#include <stdio.h>
#include <stdbool.h>

bool isValid(char* s) {
    // Write your code here
    return false;
}
`
    }
  },
  "#704": {
    name: "Binary Search",
    difficulty: "Easy",
    method_name: "search",
    tags: ["Arrays", "Binary Search"],
    constraints: [
      "1 <= nums.length <= 10^4",
      "-10^4 < nums[i], target < 10^4",
      "All the integers in nums are unique.",
      "nums is sorted in ascending order."
    ],
    hints: [
      "Since the array is sorted, we can avoid checking all elements one by one.",
      "Initialize two pointers: left at 0 and right at the end of the array. Find the middle element.",
      "If middle is target, return mid. If middle > target, move right pointer. If middle < target, move left pointer. Repeat until pointers cross."
    ],
    testcases: [
      { inputs: [[-1, 0, 3, 5, 9, 12], 9], expected: 4 },
      { inputs: [[-1, 0, 3, 5, 9, 12], 2], expected: -1 }
    ],
    hidden_testcases: [
      { inputs: [[5], 5], expected: 0 },
      { inputs: [[2, 5], 5], expected: 1 }
    ],
    desc: `Given an array of integers <code>nums</code> which is sorted in ascending order, and an integer <code>target</code>, write a function to search <code>target</code> in <code>nums</code>. If <code>target</code> exists, then return its index. Otherwise, return <code>-1</code>.<br><br>
    You must write an algorithm with <code>O(log n)</code> runtime complexity.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4</pre>`,
    stubs: {
      python: `class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # Write your code here
        pass
`,
      cpp: `#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        // Write your code here
        return -1;
    }
};
`,
      java: `class Solution {
    public int search(int[] nums, int target) {
        // Write your code here
        return -1;
    }
}
`,
      javascript: `var search = function(nums, target) {
    // Write your code here
    
};
`,
      c: `#include <stdio.h>

int search(int* nums, int numsSize, int target) {
    // Write your code here
    return -1;
}
`
    }
  },
  "#7": {
    name: "Reverse Integer",
    difficulty: "Medium",
    method_name: "reverse",
    tags: ["Math"],
    constraints: [
      "-2^31 <= x <= 2^31 - 1"
    ],
    hints: [
      "We can reverse the digits of the integer one by one using modulo (%) and division (/).",
      "Be careful of 32-bit signed integer overflow limits. If the reversed value exceeds the bounds, return 0."
    ],
    testcases: [
      { inputs: [123], expected: 321 },
      { inputs: [-123], expected: -321 }
    ],
    hidden_testcases: [
      { inputs: [120], expected: 21 },
      { inputs: [1534236469], expected: 0 }
    ],
    desc: `Given a signed 32-bit integer <code>x</code>, return <code>x</code> <em>with its digits reversed</em>. If reversing <code>x</code> causes the value to go outside the signed 32-bit integer range <code>[-2^31, 2^31 - 1]</code>, then return <code>0</code>.<br><br>
    <strong>Assume the environment does not allow you to store 64-bit integers (signed or unsigned).</strong><br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: x = 123
Output: 321</pre>`,
    stubs: {
      python: `class Solution:
    def reverse(self, x: int) -> int:
        # Write your code here
        pass
`,
      cpp: `class Solution {
public:
    int reverse(int x) {
        // Write your code here
        return 0;
    }
};
`,
      java: `class Solution {
    public int reverse(int x) {
        // Write your code here
        return 0;
    }
}
`,
      javascript: `var reverse = function(x) {
    // Write your code here
    
};
`
    }
  },
  "#9": {
    name: "Palindrome Number",
    difficulty: "Easy",
    method_name: "isPalindrome",
    tags: ["Math"],
    constraints: [
      "-2^31 <= x <= 2^31 - 1"
    ],
    hints: [
      "An integer is a palindrome when it reads the same backward as forward.",
      "Negative numbers are not palindromes due to the negative sign.",
      "Try to solve it without converting the integer to a string."
    ],
    testcases: [
      { inputs: [121], expected: true },
      { inputs: [-121], expected: false }
    ],
    hidden_testcases: [
      { inputs: [10], expected: false },
      { inputs: [0], expected: true }
    ],
    desc: `Given an integer <code>x</code>, return <code>true</code> <em>if <code>x</code> is a </em><strong><em>palindrome</em></strong><em>, and <code>false</code> otherwise</em>.<br><br>
    <strong>Example 1:</strong><br>
    <pre>Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.</pre>`,
    stubs: {
      python: `class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Write your code here
        pass
`,
      cpp: `class Solution {
public:
    bool isPalindrome(int x) {
        // Write your code here
        return false;
    }
};
`,
      java: `class Solution {
    public boolean isPalindrome(int x) {
        // Write your code here
        return false;
    }
}
`,
      javascript: `var isPalindrome = function(x) {
    // Write your code here
    
};
`
    }
  },
  "#1757": {
    name: "Recyclable and Low Fat Products",
    difficulty: "Easy",
    method_name: "query",
    tags: ["Database"],
    constraints: [
      "No custom constraints"
    ],
    hints: [
      "Filter the rows where low_fats is 'Y' and recyclable is 'Y'."
    ],
    testcases: [],
    hidden_testcases: [],
    desc: `Table: <code>Products</code><br><br>
    <pre>+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| low_fats    | enum    |
| recyclable  | enum    |
+-------------+---------+
product_id is the primary key for this table.
low_fats is an ENUM of type ('Y', 'N') where 'Y' means this product is low fat and 'N' means it is not.
recyclable is an ENUM of type ('Y', 'N') where 'Y' means this product is recyclable and 'N' means it is not.</pre><br>
    Write an SQL query to find the ids of products that are both low fat and recyclable.<br><br>
    Return the result table in any order.`,
    stubs: {
      sql: `-- Write your SQL query here
SELECT product_id FROM Products
WHERE recyclable = 'Y' AND low_fats = 'Y';
`
    }
  },
  "#584": {
    name: "Find Customer Referee",
    difficulty: "Easy",
    method_name: "query",
    tags: ["Database"],
    constraints: [
      "No custom constraints"
    ],
    hints: [
      "Be careful to handle NULL values for referee_id. In SQL, comparisons with NULL using = or != return Unknown, not True/False."
    ],
    testcases: [],
    hidden_testcases: [],
    desc: `Table: <code>Customer</code><br><br>
    <pre>+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| referee_id  | int     |
+-------------+---------+
id is the primary key column for this table.
Each row of this table indicates the id of a customer, their name, and the id of the customer who referred them.</pre><br>
    Write an SQL query to report the names of the customer that are not referred by the customer with <code>id = 2</code>.<br><br>
    Return the result table in any order.`,
    stubs: {
      sql: `-- Write your SQL query here
SELECT name FROM Customer
WHERE referee_id != 2 OR referee_id IS NULL;
`
    }
  },
  "#595": {
    name: "Big Countries",
    difficulty: "Easy",
    method_name: "query",
    tags: ["Database"],
    constraints: [
      "No custom constraints"
    ],
    hints: [
      "A country is big if it has an area of at least 3 million sq km, or a population of at least 25 million.",
      "Combine these conditions using the OR operator."
    ],
    testcases: [],
    hidden_testcases: [],
    desc: `Table: <code>World</code><br><br>
    <pre>+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name is the primary key column for this table.
Each row of this table gives information about the name of a country, the continent to which it belongs, its area, the population, and its GDP value.</pre><br>
    A country is <strong>big</strong> if:<br>
    1. it has an area of at least three million (i.e., <code>3000000 km^2</code>), or<br>
    2. it has a population of at least twenty-five million (i.e., <code>25000000</code>).<br><br>
    Write an SQL query to report the name, population, and area of the big countries.<br><br>
    Return the result table in any order.`,
    stubs: {
      sql: `-- Write your SQL query here
SELECT name, population, area FROM World
WHERE area >= 3000000 OR population >= 25000000;
`
    }
  }
};

const DSA_SOLUTIONS_DB = {
  "#1": {
    approach: "We can solve this problem optimally in <code>O(N)</code> time using a <strong>Hash Map</strong>. As we iterate through the array, we check if the complement (<code>target - nums[i]</code>) is already in our map. If it is, we return the index of the complement and the current index. Otherwise, we save the current number and its index in the map.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — We traverse the list exactly once. Each lookup and insertion in the Hash Map costs only <code>O(1)</code> on average.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — In the worst case, we store all <code>N</code> elements in the map.</li></ul>",
    diagram: `sequenceDiagram
    autonumber
    participant Loop as "Loop (nums[i])"
    participant Map as "Hash Map (val -> idx)"
    participant Ret as "Return Result"
    Note over Loop, Map: target = 9, nums = [2, 7, 11, 15]
    Loop->>Map: i = 0, val = 2: Check if complement (9 - 2 = 7) exists
    Map-->>Loop: Not found
    Loop->>Map: Put 2 to 0
    Loop->>Map: i = 1, val = 7: Check if complement (9 - 7 = 2) exists
    Map-->>Loop: Found value 2 at index 0!
    Loop->>Ret: Return [0, 1]`,
    code: {
      python: `def twoSum(nums: list[int], target: int) -> list[int]:
    prevMap = {}  # value -> index
    for i, n in enumerate(nums):
        diff = target - n
        if diff in prevMap:
            return [prevMap[diff], i]
        prevMap[n] = i
    return []`,
      cpp: `vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> prevMap; // value -> index
    for (int i = 0; i < nums.size(); i++) {
        int diff = target - nums[i];
        if (prevMap.find(diff) != prevMap.end()) {
            return {prevMap[diff], i};
        }
        prevMap[nums[i]] = i;
    }
    return {};
}`,
      java: `public int[] twoSum(int[] nums, int target) {
    HashMap<Integer, Integer> prevMap = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int diff = target - nums[i];
        if (prevMap.containsKey(diff)) {
            return new int[] { prevMap.get(diff), i };
        }
        prevMap.put(nums[i], i);
    }
    return new int[0];
}`,
      javascript: `var twoSum = function(nums, target) {
    const prevMap = {}; // value -> index
    for (let i = 0; i < nums.length; i++) {
        const diff = target - nums[i];
        if (diff in prevMap) {
            return [prevMap[diff], i];
        }
        prevMap[nums[i]] = i;
    }
    return [];
};`
    }
  },
  "#217": {
    approach: "The most efficient way to check for duplicates is using a <strong>Hash Set</strong>. We initialize an empty set and iterate through the array. For each number, we check if it is already in the set. If it is, we return <code>true</code> immediately. If we reach the end of the array without finding any duplicates, we return <code>false</code>.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — We iterate through the array once and check/insert in the set in <code>O(1)</code> average time.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — We store up to <code>N</code> unique elements in the set.</li></ul>",
    diagram: `flowchart TD
    Start([Start]) --> Init[Initialize Hash Set]
    Init --> Loop{For each num in nums}
    Loop -- Yes --> Check{num already in Set?}
    Check -- Yes --> RetTrue[Return true]
    Check -- No --> Add[Add num to Set]
    Add --> Loop
    Loop -- No --> RetFalse[Return false]`,
    code: {
      python: `def containsDuplicate(nums: list[int]) -> bool:
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False`,
      cpp: `bool containsDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    for (int n : nums) {
        if (seen.find(n) != seen.end()) {
            return true;
        }
        seen.insert(n);
    }
    return false;
}`,
      java: `public boolean containsDuplicate(int[] nums) {
    HashSet<Integer> seen = new HashSet<>();
    for (int n : nums) {
        if (seen.contains(n)) {
            return true;
        }
        seen.add(n);
    }
    return false;
}`,
      javascript: `var containsDuplicate = function(nums) {
    const seen = new Set();
    for (let n of nums) {
        if (seen.has(n)) {
            return true;
        }
        seen.add(n);
    }
    return false;
};`
    }
  },
  "#242": {
    approach: "An anagram is a rearrangement of characters. If string <code>s</code> and <code>t</code> have different lengths, they cannot be anagrams. We can use a <strong>Frequency Array of size 26</strong> to count character occurrences. We increment count for characters in <code>s</code> and decrement for characters in <code>t</code>. Finally, we verify if all indices in our frequency table are zero.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — We iterate over both strings of length <code>N</code> once, and then do a constant O(26) pass over the frequency array.</li><li><strong>Space Complexity:</strong> <code>O(1)</code> — The space is fixed to 26 characters (lowercase letters), which does not scale with input length.</li></ul>",
    diagram: `flowchart TD
    Start([Start]) --> LenCheck{"Length s == t?"}
    LenCheck -- No --> RetFalse["Return false"]
    LenCheck -- Yes --> Init["Init Frequency Array size 26"]
    Init --> Loop1{"For each char in s, t"}
    Loop1 -- Yes --> IncDec["Increment count for s[i], Decrement count for t[i]"]
    IncDec --> Loop1
    Loop1 -- No --> Loop2{"All elements in Array == 0?"}
    Loop2 -- Yes --> RetTrue["Return true"]
    Loop2 -- No --> RetFalse`,
    code: {
      python: `def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = {}
    for i in range(len(s)):
        count[s[i]] = count.get(s[i], 0) + 1
        count[t[i]] = count.get(t[i], 0) - 1
    for char in count:
        if count[char] != 0:
            return False
    return True`,
      cpp: `bool isAnagram(string s, string t) {
    if (s.length() != t.length()) return false;
    vector<int> count(26, 0);
    for (int i = 0; i < s.length(); i++) {
        count[s[i] - 'a']++;
        count[t[i] - 'a']--;
    }
    for (int val : count) {
        if (val != 0) return false;
    }
    return true;
}`,
      java: `public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i) - 'a']++;
        count[t.charAt(i) - 'a']--;
    }
    for (int val : count) {
        if (val != 0) return false;
    }
    return true;
}`,
      javascript: `var isAnagram = function(s, t) {
    if (s.length !== t.length) return false;
    const count = {};
    for (let i = 0; i < s.length; i++) {
        count[s[i]] = (count[s[i]] || 0) + 1;
        count[t[i]] = (count[t[i]] || 0) - 1;
    }
    for (let key in count) {
        if (count[key] !== 0) return false;
    }
    return true;
};`
    }
  },
  "#20": {
    approach: "We use a <strong>Stack</strong> to keep track of open brackets. When we encounter an opening bracket, we push it to the stack. When we encounter a closing bracket, we check if the stack is empty or if the top of the stack matches its opening pair. If it does not, the string is invalid. Finally, if the stack is completely empty, all brackets have been closed in matching order.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — We traverse the string of length <code>N</code> once, and each push/pop operation on stack takes <code>O(1)</code> time.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — In the worst case, we push all opening brackets onto the stack (e.g. <code>'(((((('</code>).</li></ul>",
    diagram: `sequenceDiagram
    participant Char as "Character Input"
    participant Stk as "Stack (LIFO)"
    participant Check as "Validity Checker"
    Char->>Stk: i=0: Encounter '(' then Push
    Char->>Stk: i=1: Encounter '[' then Push
    Char->>Check: i=2: Encounter ']' then Check top
    Stk-->>Check: Top is '[' (Match!)
    Check->>Stk: Pop top '['
    Char->>Check: i=3: Encounter ')' then Check top
    Stk-->>Check: Top is '(' (Match!)
    Check->>Stk: Pop top '('
    Note over Stk: Stack is empty and Valid!`,
    code: {
      python: `def isValid(s: str) -> bool:
    stack = []
    closeToOpen = { ")": "(", "]": "[", "}": "{" }
    for c in s:
        if c in closeToOpen:
            if stack and stack[-1] == closeToOpen[c]:
                stack.pop()
            else:
                return False
        else:
            stack.append(c)
    return True if not stack else False`,
      cpp: `bool isValid(string s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.empty()) return false;
            if (c == ')' && st.top() != '(') return false;
            if (c == ']' && st.top() != '[') return false;
            if (c == '}' && st.top() != '{') return false;
            st.pop();
        }
    }
    return st.empty();
}`,
      java: `public boolean isValid(String s) {
    Stack<Character> stack = new Stack<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char top = stack.peek();
            if ((c == ')' && top == '(') || 
                (c == ']' && top == '[') || 
                (c == '}' && top == '{')) {
                stack.pop();
            } else {
                return false;
            }
        }
    }
    return stack.isEmpty();
}`,
      javascript: `var isValid = function(s) {
    const stack = [];
    const mapping = { ')': '(', ']': '[', '}': '{' };
    for (let c of s) {
        if (c in mapping) {
            if (stack.length && stack[stack.length - 1] === mapping[c]) {
                stack.pop();
            } else {
                return false;
            }
        } else {
            stack.push(c);
        }
    }
    return stack.length === 0;
};`
    }
  },
  "#704": {
    approach: "Binary Search is a divide-and-conquer algorithm for sorted arrays. We define two pointers: <code>left = 0</code> and <code>right = nums.length - 1</code>. In each step, we calculate the middle index <code>mid = left + (right - left) / 2</code>. If <code>nums[mid] == target</code>, we return the index. If it is less, we search the right half by updating <code>left = mid + 1</code>. If it is greater, we search the left half by updating <code>right = mid - 1</code>.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(log N)</code> — The search space is halved in every iteration.</li><li><strong>Space Complexity:</strong> <code>O(1)</code> — We only use pointers which take constant space.</li></ul>",
    diagram: `flowchart TD
    Start([Start]) --> Init["left = 0, right = n-1"]
    Init --> Loop{"left <= right"}
    Loop -- Yes --> Mid["mid = left + (right-left) / 2"]
    Mid --> Check{"nums[mid] == target?"}
    Check -- Yes --> RetIdx["Return mid"]
    Check -- No --> CheckLess{"nums[mid] < target?"}
    CheckLess -- Yes --> SetLeft["left = mid + 1"]
    CheckLess -- No --> SetRight["right = mid - 1"]
    SetLeft --> Loop
    SetRight --> Loop
    Loop -- No --> RetMinus1["Return -1"]`,
    code: {
      python: `def search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return -1`,
      cpp: `int search(vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
}`,
      java: `public int search(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
}`,
      javascript: `var search = function(nums, target) {
    let l = 0, r = nums.length - 1;
    while (l <= r) {
        const mid = l + Math.floor((r - l) / 2);
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
};`
    }
  },
  "#7": {
    approach: "We can reverse the integer mathematically. By using modulo 10 (<code>x % 10</code>), we extract the last digit. We then append this digit to our reversed number (<code>rev = rev * 10 + digit</code>) and divide our number by 10. To prevent overflow in 32-bit systems, we must check if <code>rev</code> is about to exceed <code>[-2^31, 2^31 - 1]</code> before multiplying by 10.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(log10(x))</code> — The number of digits in <code>x</code> is approximately <code>log10(x)</code>.</li><li><strong>Space Complexity:</strong> <code>O(1)</code> — We only use variables that take constant space.</li></ul>",
    diagram: `flowchart TD
    Start([Start]) --> CheckSign["Save sign of x"]
    CheckSign --> Mod["Get digits: rev = rev * 10 + x % 10"]
    Mod --> CheckBound{"Check if rev outside [-2^31, 2^31-1]"}
    CheckBound -- Yes --> Return0["Return 0"]
    CheckBound -- No --> CheckEmpty{"x == 0?"}
    CheckEmpty -- No --> Mod
    CheckEmpty -- Yes --> Final["Apply sign and return rev"]`,
    code: {
      python: `def reverse(x: int) -> int:
    MIN_INT, MAX_INT = -2**31, 2**31 - 1
    rev = 0
    sign = -1 if x < 0 else 1
    x = abs(x)
    while x != 0:
        digit = x % 10
        x //= 10
        # Check bounds
        if rev > (MAX_INT - digit) // 10:
            return 0
        rev = rev * 10 + digit
    return sign * rev`,
      cpp: `int reverse(int x) {
    int rev = 0;
    while (x != 0) {
        int pop = x % 10;
        x /= 10;
        if (rev > INT_MAX/10 || (rev == INT_MAX / 10 && pop > 7)) return 0;
        if (rev < INT_MIN/10 || (rev == INT_MIN / 10 && pop < -8)) return 0;
        rev = rev * 10 + pop;
    }
    return rev;
}`,
      java: `public int reverse(int x) {
    int rev = 0;
    while (x != 0) {
        int pop = x % 10;
        x /= 10;
        if (rev > Integer.MAX_VALUE/10 || (rev == Integer.MAX_VALUE/10 && pop > 7)) return 0;
        if (rev < Integer.MIN_VALUE/10 || (rev == Integer.MIN_VALUE/10 && pop < -8)) return 0;
        rev = rev * 10 + pop;
    }
    return rev;
}`,
      javascript: `var reverse = function(x) {
    const LIMIT = Math.pow(2, 31);
    let rev = 0;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    while (x > 0) {
        const digit = x % 10;
        rev = rev * 10 + digit;
        x = Math.floor(x / 10);
    }
    rev = sign * rev;
    if (rev < -LIMIT || rev > LIMIT - 1) return 0;
    return rev;
};`
    }
  },
  "#9": {
    approach: "Instead of converting the number to a string, we can reverse the second half of the number and compare it with the first half. For example, for <code>1221</code>, we reverse the last two digits to get <code>21</code>, and compare it with the first half <code>12</code>. If they are equal, the number is a palindrome.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(log10(N))</code> — We only iterate through half of the digits.</li><li><strong>Space Complexity:</strong> <code>O(1)</code> — constant space.</li></ul>",
    diagram: `flowchart TD
    Start([Start]) --> NegCheck{"Is x < 0 or ends in 0 except 0?"}
    NegCheck -- Yes --> RetFalse["Return false"]
    NegCheck -- No --> Loop{"While x > rev"}
    Loop -- Yes --> Mod["rev = rev * 10 + x % 10; x = x / 10"]
    Mod --> Loop
    Loop -- No --> Compare{"Is x == rev or x == rev/10?"}
    Compare -- Yes --> RetTrue["Return true"]
    Compare -- No --> RetFalse`,
    code: {
      python: `def isPalindrome(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    rev = 0
    while x > rev:
        rev = rev * 10 + x % 10
        x //= 10
    return x == rev or x == rev // 10`,
      cpp: `bool isPalindrome(int x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) return false;
    int rev = 0;
    while (x > rev) {
        rev = rev * 10 + x % 10;
        x /= 10;
    }
    return x == rev || x == rev / 10;
}`,
      java: `public boolean isPalindrome(int x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) return false;
    int rev = 0;
    while (x > rev) {
        rev = rev * 10 + (x % 10);
        x /= 10;
    }
    return x == rev || x == rev / 10;
}`,
      javascript: `var isPalindrome = function(x) {
    if (x < 0 || (x % 10 === 0 && x !== 0)) return false;
    let rev = 0;
    while (x > rev) {
        rev = rev * 10 + (x % 10);
        x = Math.floor(x / 10);
    }
    return x === rev || x === Math.floor(rev / 10);
};`
    }
  },
  "#1757": {
    approach: "This is a simple filter database query. In SQL, we use the <code>WHERE</code> clause to filter the products that have both properties: <code>recyclable = 'Y'</code> and <code>low_fats = 'Y'</code>.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — The database does a scan over <code>N</code> records in the table.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — To return the results matching the query constraints.</li></ul>",
    diagram: `flowchart TD
    Start([Table Products]) --> Filter["Filter: low_fats = 'Y' and recyclable = 'Y'"]
    Filter --> Project["Select product_id"]
    Project --> Output([Result Set])`,
    code: {
      sql: `SELECT product_id FROM Products
WHERE low_fats = 'Y' AND recyclable = 'Y';`
    }
  },
  "#584": {
    approach: "We need to filter names from the Customer table where <code>referee_id != 2</code>. However, standard comparisons like <code>referee_id != 2</code> ignore <code>NULL</code> values since comparisons with NULL result in <code>UNKNOWN</code>. We must explicitly include customers with no referee using <code>referee_id IS NULL</code>.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — Full table scan of Customer rows.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — Outputs matching customers.</li></ul>",
    diagram: `flowchart TD
    Start([Table Customer]) --> Filter["Filter: referee_id != 2 OR referee_id IS NULL"]
    Filter --> Project["Select name"]
    Project --> Output([Result Set])`,
    code: {
      sql: `SELECT name FROM Customer
WHERE referee_id != 2 OR referee_id IS NULL;`
    }
  },
  "#595": {
    approach: "We use the logical operator <code>OR</code> to find countries matching either condition: having an area greater than or equal to 3,000,000, or a population greater than or equal to 25,000,000.",
    complexity: "<ul><li><strong>Time Complexity:</strong> <code>O(N)</code> — Standard table scan.</li><li><strong>Space Complexity:</strong> <code>O(N)</code> — Stores result set.</li></ul>",
    diagram: `flowchart TD
    Start([Table World]) --> Filter["Filter: area >= 3,000,000 OR population >= 25,000,000"]
    Filter --> Project["Select name, population, area"]
    Project --> Output([Result Set])`,
    code: {
      sql: `SELECT name, population, area FROM World
WHERE area >= 3000000 OR population >= 25000000;`
    }
  }
};
