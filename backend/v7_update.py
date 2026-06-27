import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

html_file = os.path.join(FRONTEND, "htmlfresher.html")
with open(html_file, "r") as f:
    html_content = f.read()

# 1. Update Tracker Block Numbers to NOT be colourful
# Find: <div class="acc-block-num" style="background:#XXXXXX">
# Replace with: <div class="acc-block-num" style="background:var(--text-1); color:var(--bg);">
html_content = re.sub(
    r'<div class="acc-block-num" style="background:#[a-fA-F0-9]+">',
    r'<div class="acc-block-num" style="background:var(--text-1); color:var(--bg);">',
    html_content
)

with open(html_file, "w") as f:
    f.write(html_content)

# 2. Re-create interview_qa.html matching GrindOS theme exactly
topbar_html = """
  <header class="topbar">
    <a href="dashboard.html" class="topbar-brand">
      <img src="/logo.png" alt="GrindOS Logo" class="brand-logo"
        style="width: 34px; height: 34px; object-fit: contain; border-radius: 4px; flex-shrink: 0; display: inline-block; vertical-align: middle; margin-right: 4px;">
      <span class="brand-wordmark">GrindOS</span>
    </a>
    <nav class="topbar-nav">
      <a href="dashboard.html" class="learn-nav">Learn</a>
      <a href="notes.html" class="notes-nav">Notes</a>
      <a href="htmlfresher.html" class="tracker-nav active">Tracker</a>
      <a href="practice.html" class="practice-nav">Practice</a>
      <a href="resume-builder.html" class="resume-nav">Resume</a>
      <a href="daily-checkin.html" class="checkin-nav">Check In</a>
    </nav>
    <div class="topbar-right">
      <button class="icon-btn" id="theme-toggle" aria-label="Toggle theme"><span class="theme-icon">☾</span></button>
      <div id="clerk-user-widget"></div>
    </div>
  </header>
"""

blocks = [
  {
    "topics": [
      {"name":"Variables, types, loops, conditionals", "q":"What's the diff between a list and a tuple?", "a":"List is mutable (can be changed), tuple is immutable. Tuples are faster and used for fixed data.", "tip":"Always mention immutability as a feature for safety and memory efficiency, not just a restriction."},
      {"name":"Functions + scope + comprehensions", "q":"What is a closure?", "a":"A function that remembers its enclosing scope (variables) even after the outer function has returned.", "tip":"Explain it simply: 'It's a function that comes with its own backpack of variables.'"},
      {"name":"Data structures built-in", "q":"When would you use a set over a list?", "a":"When you need O(1) lookup time, automatic deduplication, or to perform fast membership tests.", "tip":"Interviewers love when you explicitly state 'O(1) average case lookup' vs 'O(n) for lists'."},
      {"name":"Strings + file handling + exceptions", "q":"What does 'with open()' do differently?", "a":"It's a context manager that automatically closes the file for you, even if an error occurs inside the block.", "tip":"Use the term 'Context Manager' and mention the __enter__ and __exit__ dunder methods to impress them."},
      {"name":"Modules, stdlib, decorators intro", "q":"What is a decorator?", "a":"A function that wraps another function to modify or extend its behaviour without changing its source code.", "tip":"Say it's the 'Open-Closed Principle' in practice (open for extension, closed for modification)."},
      {"name":"Classes, objects, __init__, self", "q":"What is 'self'?", "a":"It's a reference to the current instance of the class. Python doesn't pass it implicitly like Java's 'this'.", "tip":"Mention that 'self' isn't a keyword, it's just a convention. You could name it 'this' or 'me', but PEP 8 dictates 'self'."},
      {"name":"Encapsulation + inheritance", "q":"What is MRO?", "a":"Method Resolution Order. It determines which parent method is called in multiple inheritance using C3 linearisation.", "tip":"Drop the term 'C3 linearisation' casually. It shows deep language knowledge."},
      {"name":"Polymorphism + abstraction", "q":"Abstraction vs encapsulation?", "a":"Encapsulation is HOW you hide (bundling data/methods). Abstraction is WHAT you hide (exposing only relevant interface).", "tip":"Use the TV remote analogy: Encapsulation hides the circuits, Abstraction gives you just the power button."},
      {"name":"Dunder methods + class/static methods", "q":"When use @staticmethod vs @classmethod?", "a":"Static method has no access to class/instance. Class method gets 'cls', useful for factory methods.", "tip":"Give an example: @classmethod for alternative constructors (e.g., from_json), @staticmethod for utility math functions."},
      {"name":"Decorators deep dive", "q":"What is a decorator really?", "a":"It's syntactic sugar. '@dec def f()' is exactly the same as 'f = dec(f)'.", "tip":"Explain that functions in Python are first-class objects (can be passed around as arguments)."},
      {"name":"Arrays + strings", "q":"Why is string concatenation O(n²) in a loop?", "a":"Strings are immutable. Each '+' creates a completely new string in memory. Use ''.join() instead.", "tip":"This is a classic 'Do you know how memory works' question. Never use '+=' for strings in a loop."},
      {"name":"Stack + queue", "q":"When do you use a stack?", "a":"Undo/redo features, expression evaluation (brackets), DFS traversal, and backtracking algorithms.", "tip":"Say 'LIFO' explicitly. Mention the browser history button as a real-world example."},
      {"name":"Linked list", "q":"How detect a cycle in linked list?", "a":"Floyd's tortoise and hare algorithm. A fast (2 steps) and slow (1 step) pointer will eventually meet if a cycle exists.", "tip":"Don't just code it, explain WHY they meet (the relative speed is 1 node per step)."},
      {"name":"HashMap + set", "q":"When does O(1) break for HashMap?", "a":"During a hash collision, making worst case O(n). Python dict uses open addressing to resolve collisions.", "tip":"Knowing that Python uses Open Addressing (probing) rather than Chaining sets you apart from Java devs."},
      {"name":"Binary tree + BST", "q":"What makes a valid BST?", "a":"All nodes in the left subtree must be < node, and all right subtree nodes > node. Not just immediate children!", "tip":"Interviewers will try to trick you with a tree where immediate children are valid, but a deep child breaks the rule."},
      {"name":"Heap + priority queue", "q":"How to get K largest elements efficiently?", "a":"Use a min-heap of size K. It takes O(n log K) which is much faster than O(n log n) sorting.", "tip":"Explain that sorting the whole array does unnecessary work for elements outside the top K."},
      {"name":"Graphs (BFS + DFS)", "q":"BFS vs DFS — when to use which?", "a":"BFS for shortest path in unweighted graphs. DFS for cycle detection, topological sort, and maze solving.", "tip":"Mention their underlying data structures: BFS uses a Queue, DFS uses a Stack (or recursion call stack)."},
      {"name":"Trie", "q":"Why use a Trie over HashMap for prefix search?", "a":"Trie gives prefix matching natively in O(m) time where m is word length. HashMap requires scanning all keys.", "tip":"Mention real-world use cases: Autocomplete, spell checkers, and IP routing."},
      {"name":"Two pointers", "q":"When should you think of two pointers?", "a":"When dealing with a sorted array, or when you need to find a pair/triplet that meets a condition.", "tip":"Always check if sorting the array first makes it a two-pointer problem (e.g., 3Sum)."},
      {"name":"Sliding window", "q":"When to use sliding window?", "a":"Any contiguous subarray or substring problem. Figure out if the window needs to be fixed size or variable.", "tip":"Say 'It optimises an O(n²) brute force approach to O(n) by not re-calculating overlapping parts'."},
      {"name":"Binary search", "q":"When to use binary search on the answer?", "a":"When you are searching for a minimum/maximum value (like capacity or speed) rather than an index position.", "tip":"Look for problems asking for 'minimum maximum' or 'maximum minimum'."},
      {"name":"Sorting algorithms", "q":"Why is merge sort preferred over quick sort sometimes?", "a":"Merge sort guarantees O(n log n) worst case. Quick sort can degrade to O(n²) with a bad pivot choice.", "tip":"Also mention that Merge Sort is stable, while standard Quick Sort is not."},
      {"name":"Recursion + call stack", "q":"What is tail recursion?", "a":"When the recursive call is the absolute last operation. Note: standard Python doesn't optimise tail recursion.", "tip":"Knowing that Python lacks TCO (Tail Call Optimisation) unlike C/C++ shows deep language insight."},
      {"name":"Backtracking", "q":"How to identify backtracking?", "a":"If the problem asks to 'generate all possible' permutations, combinations, or subsets. Try → recurse → undo.", "tip":"Always write a helper function explicitly named 'backtrack' or 'explore' to show clear intent."},
      {"name":"Dynamic programming", "q":"When is DP the right approach?", "a":"When you see overlapping subproblems + optimal substructure. If you draw a recursion tree and see repeated nodes, use DP.", "tip":"Don't just say 'DP'. Explain whether you'd use Top-Down (Memoization) or Bottom-Up (Tabulation)."},
      {"name":"Greedy", "q":"How do you know greedy works vs DP?", "a":"Greedy works when making the local optimal choice leads to the global optimal solution. Prove it with an exchange argument.", "tip":"If a problem asks for optimal solution but seems too complex for DP (e.g. interval scheduling), try greedy."},
      {"name":"Graph algorithms", "q":"When does Dijkstra fail?", "a":"It fails when there are negative weight edges. You must use Bellman-Ford instead.", "tip":"Explain why: Dijkstra assumes that adding another edge always increases total distance."},
      {"name":"Bit manipulation", "q":"XOR trick for finding a single duplicate?", "a":"Since a ^ a = 0, XOR all elements with 1..n. Everything cancels out except the duplicate.", "tip":"Always trace it out on a whiteboard: 3^3 = 0, so [2,3,4,3] ^ [2,3,4] leaves just the extra 3."},
      {"name":"OS — processes and threads", "q":"Process vs thread in one line?", "a":"A process has its own memory space, while threads share memory within the same process.", "tip":"Mention that threads are 'lightweight' because context switching doesn't require flushing the TLB (Translation Lookaside Buffer)."},
      {"name":"OS — deadlock", "q":"4 conditions for deadlock?", "a":"Mutual exclusion, hold and wait, no preemption, and circular wait. All four must be true.", "tip":"Mention 'Coffman conditions' by name. To prevent deadlock, you just need to break ONE of these four."},
      {"name":"OS — memory management", "q":"What is thrashing?", "a":"When a process spends more time paging (swapping memory to disk) than executing due to low RAM.", "tip":"Use the term 'Page Fault'. High page fault rate = thrashing."},
      {"name":"DBMS — ER, normalisation", "q":"3NF vs BCNF?", "a":"3NF allows some redundancy for lossless joins. BCNF is stricter: every determinant must be a candidate key.", "tip":"Don't just recite definitions. Explain that BCNF fixes the edge case where 3NF fails due to overlapping candidate keys."},
      {"name":"DBMS — SQL deep dive", "q":"WHERE vs HAVING?", "a":"WHERE filters rows before grouping. HAVING filters after GROUP BY. You can't use aggregates in WHERE.", "tip":"Explain the SQL execution order to prove you understand it (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT)."},
      {"name":"DBMS — transactions", "q":"What is a dirty read?", "a":"When a transaction reads uncommitted data from another transaction. Prevented by 'Read Committed' isolation level.", "tip":"Link it to ACID properties (specifically Isolation)."},
      {"name":"Computer networks", "q":"What layer does HTTP work at?", "a":"Application layer (Layer 7). TCP is Transport (Layer 4). IP is Network (Layer 3).", "tip":"Mention the OSI model explicitly. Bonus points if you know the exact layer of SSL/TLS (Layer 6 Presentation / between 4 and 7)."},
      {"name":"System design basics", "q":"Design a URL shortener flow", "a":"Hash function → 6-char code → store long:short in DB → redirect via lookup. Add caching for hot URLs.", "tip":"Always mention potential bottlenecks and how to scale (e.g. read-heavy, so use Redis)."},
      {"name":"HTML/CSS + JS fundamentals", "q":"What is the event loop?", "a":"JS is single-threaded. The event loop picks tasks from the queue and executes them only when the call stack is empty.", "tip":"Draw it out: Call Stack <-> Web APIs <-> Callback Queue. Mention Microtasks vs Macrotasks."},
      {"name":"React hooks", "q":"useEffect vs useLayoutEffect?", "a":"useLayoutEffect fires synchronously before browser paint. useEffect fires asynchronously after paint. Default to useEffect.", "tip":"Mention that useLayoutEffect is only for preventing visual flickering when mutating the DOM directly."},
      {"name":"REST API design", "q":"PUT vs PATCH?", "a":"PUT replaces the entire resource. PATCH updates partial fields. Most APIs misuse PUT for partial updates.", "tip":"Say 'PUT is idempotent. If you send the same PUT request 10 times, the result is exactly the same.'"},
      {"name":"Git advanced", "q":"Rebase vs merge?", "a":"Rebase rewrites commit history for a clean linear log. Merge preserves history with a merge commit. Never rebase public branches.", "tip":"'Never rebase a public branch' is the golden rule. Saying this shows you have actual team experience."},
      {"name":"Math foundation", "q":"What is gradient descent?", "a":"Iteratively moving in the direction of steepest descent of a loss function to find the minimum. Step size = learning rate.", "tip":"Compare it to walking down a mountain blindfolded, taking steps in the steepest downward direction."},
      {"name":"Classical ML", "q":"Bias vs variance tradeoff?", "a":"High bias = underfitting (too simple). High variance = overfitting (too complex/noisy). Goal is to find the sweet spot.", "tip":"Use the bullseye analogy: High bias is missing the target consistently. High variance is hitting randomly all over."},
      {"name":"Evaluation metrics", "q":"When is F1 better than accuracy?", "a":"On imbalanced datasets. Accuracy is misleading when one class dominates. F1 balances precision and recall.", "tip":"Example: Fraud detection. 99% of transactions aren't fraud. A model that always predicts 'not fraud' is 99% accurate, but useless."},
      {"name":"Neural networks", "q":"Why ReLU over sigmoid?", "a":"Sigmoid suffers from vanishing gradients in deep networks. ReLU gradient is 1 for positive values, preventing vanishing.", "tip":"Also mention that ReLU is computationally much cheaper (just a max(0, x) operation)."},
      {"name":"Transformers", "q":"What problem does attention solve?", "a":"RNNs forget long-range dependencies. Attention lets every token look at every other token simultaneously.", "tip":"Say 'It solved the information bottleneck problem of seq2seq models'."},
      {"name":"RAG", "q":"RAG vs fine-tuning?", "a":"RAG injects knowledge at inference time (best for changing data). Fine-tuning changes model weights (best for format/style).", "tip":"Compare it to taking an open-book exam (RAG) vs studying really hard beforehand (Fine-tuning)."},
      {"name":"LLM agents", "q":"What is an LLM agent?", "a":"An LLM with access to external tools (like search/calc), capable of taking actions based on a reasoning loop (ReAct).", "tip":"Mention the ReAct framework explicitly (Reason -> Act -> Observe)."},
      {"name":"MLOps", "q":"What is model drift?", "a":"When a model's performance degrades over time because the real-world data distribution shifted away from the training data.", "tip":"Mention Data Drift vs Concept Drift to show nuanced understanding."}
    ]
  }
]

qa_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Interview Q&A Bank</title>
    <!-- Use same stylesheet for consistency -->
    <link rel="stylesheet" href="assets/style.css">
    <style>
        /* Specific page overrides to match GrindOS styling while being one cohesive block */
        .qa-container {{ max-width: 960px; margin: 4rem auto; padding: 0 1.5rem 6rem; }}
        .qa-hero {{ margin-bottom: 3rem; text-align: center; }}
        .qa-hero h1 {{ font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 12px; letter-spacing: -0.02em; }}
        .qa-hero p {{ font-size: 1.1rem; color: var(--text-secondary); max-width: 650px; margin: 0 auto; line-height: 1.6; }}
        
        .qa-grid {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .qa-card {{
            background: var(--surface-1);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.75rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.02);
            transition: all 0.2s;
            position: relative;
            overflow: hidden;
        }}
        
        .qa-card:hover {{
            border-color: var(--border-strong);
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            transform: translateY(-2px);
        }}
        
        /* Subtle left accent */
        .qa-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--text-1);
            border-radius: 4px 0 0 4px;
            opacity: 0.1;
        }}
        
        .qa-q {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }}
        .qa-q-icon {{ color: var(--text-1); flex-shrink: 0; }}
        
        .qa-a {{
            font-size: 1rem;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 16px;
            padding-left: 32px;
        }}
        
        .qa-premium-tip {{
            background: rgba(255, 94, 0, 0.05);
            border: 1px solid rgba(255, 94, 0, 0.2);
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-left: 32px;
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }}
        .qa-premium-tip-icon {{
            color: var(--brand);
            font-size: 1.2rem;
            margin-top: 2px;
        }}
        .qa-premium-tip-text {{
            font-size: 0.95rem;
            color: var(--text-primary);
            line-height: 1.5;
        }}
        .qa-premium-tip-text b {{ color: var(--brand); font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; display: block; margin-bottom: 4px; }}
        
    </style>
</head>
<body>
    {topbar_html}
    
    <div class="qa-container">
        <div class="qa-hero">
            <h1>Ultimate Interview Q&A</h1>
            <p>Don't just answer the question — dominate it. These are the top 50 high-yield questions across all CS domains, formulated with premium interview strategies that signal deep expertise.</p>
        </div>
        
        <div class="qa-grid">
"""

for t in blocks[0]["topics"]:
    qa_html += f"""
            <div class="qa-card">
                <div class="qa-q"><span class="qa-q-icon">Q.</span> {t['q']}</div>
                <div class="qa-a">{t['a']}</div>
                <div class="qa-premium-tip">
                    <span class="qa-premium-tip-icon">💡</span>
                    <div class="qa-premium-tip-text">
                        <b>Premium Strategy</b>
                        {t['tip']}
                    </div>
                </div>
            </div>"""

qa_html += """
        </div>
    </div>
    
    <script>
      (function() {
        const toggle = document.getElementById('theme-toggle');
        if(toggle) {
          toggle.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('GrindOS-theme', isDark ? 'dark' : '');
          });
        }
      })();
    </script>
</body>
</html>
"""

with open(os.path.join(FRONTEND, "interview_qa.html"), "w") as f:
    f.write(qa_html)

print("Update 7 complete: Block colors neutral, Q&A page fully integrated with GrindOS theme.")
