import os
import re
import json

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# 1. Re-extract topics to get the Q&A data for the new page
blocks = [
  {
    "num": 1, "title": "Python Foundation", "color": "#7C6EE0",
    "topics": [
      {"name":"Variables, types, loops, conditionals", "q":"What's the diff between a list and a tuple?", "a":"List is mutable (can be changed), tuple is immutable. Tuples are faster and used for fixed data."},
      {"name":"Functions + scope + comprehensions", "q":"What is a closure?", "a":"A function that remembers its enclosing scope (variables) even after the outer function has returned."},
      {"name":"Data structures built-in", "q":"When would you use a set over a list?", "a":"When you need O(1) lookup time, automatic deduplication, or to perform fast membership tests."},
      {"name":"Strings + file handling + exceptions", "q":"What does 'with open()' do differently?", "a":"It's a context manager that automatically closes the file for you, even if an error occurs inside the block."},
      {"name":"Modules, stdlib, decorators intro", "q":"What is a decorator?", "a":"A function that wraps another function to modify or extend its behaviour without changing its source code."},
    ]
  },
  {
    "num": 2, "title": "Object Oriented Programming", "color": "#0F6E56",
    "topics": [
      {"name":"Classes, objects, __init__, self", "q":"What is 'self'?", "a":"It's a reference to the current instance of the class. Python doesn't pass it implicitly like Java's 'this'."},
      {"name":"Encapsulation + inheritance", "q":"What is MRO?", "a":"Method Resolution Order. It determines which parent method is called in multiple inheritance using C3 linearisation."},
      {"name":"Polymorphism + abstraction", "q":"Abstraction vs encapsulation?", "a":"Encapsulation is HOW you hide (bundling data/methods). Abstraction is WHAT you hide (exposing only relevant interface)."},
      {"name":"Dunder methods + class/static methods", "q":"When use @staticmethod vs @classmethod?", "a":"Static method has no access to class/instance. Class method gets 'cls', useful for factory methods."},
      {"name":"Decorators deep dive", "q":"What is a decorator really?", "a":"It's syntactic sugar. '@dec def f()' is exactly the same as 'f = dec(f)'."},
    ]
  },
  {
    "num": 3, "title": "Data Structures", "color": "#993C1D",
    "topics": [
      {"name":"Arrays + strings", "q":"Why is string concatenation O(n²) in a loop?", "a":"Strings are immutable. Each '+' creates a completely new string in memory. Use ''.join() instead."},
      {"name":"Stack + queue", "q":"When do you use a stack?", "a":"Undo/redo features, expression evaluation (brackets), DFS traversal, and backtracking algorithms."},
      {"name":"Linked list", "q":"How detect a cycle in linked list?", "a":"Floyd's tortoise and hare algorithm. A fast (2 steps) and slow (1 step) pointer will eventually meet if a cycle exists."},
      {"name":"HashMap + set", "q":"When does O(1) break for HashMap?", "a":"During a hash collision, making worst case O(n). Python dict uses open addressing to resolve collisions."},
      {"name":"Binary tree + BST", "q":"What makes a valid BST?", "a":"All nodes in the left subtree must be < node, and all right subtree nodes > node. Not just immediate children!"},
      {"name":"Heap + priority queue", "q":"How to get K largest elements efficiently?", "a":"Use a min-heap of size K. It takes O(n log K) which is much faster than O(n log n) sorting."},
      {"name":"Graphs (BFS + DFS)", "q":"BFS vs DFS — when to use which?", "a":"BFS for shortest path in unweighted graphs. DFS for cycle detection, topological sort, and maze solving."},
      {"name":"Trie", "q":"Why use a Trie over HashMap for prefix search?", "a":"Trie gives prefix matching natively in O(m) time where m is word length. HashMap requires scanning all keys."},
    ]
  },
  {
    "num": 4, "title": "DSA Problem Patterns", "color": "#A32D2D",
    "topics": [
      {"name":"Two pointers", "q":"When should you think of two pointers?", "a":"When dealing with a sorted array, or when you need to find a pair/triplet that meets a condition."},
      {"name":"Sliding window", "q":"When to use sliding window?", "a":"Any contiguous subarray or substring problem. Figure out if the window needs to be fixed size or variable."},
      {"name":"Binary search", "q":"When to use binary search on the answer?", "a":"When you are searching for a minimum/maximum value (like capacity or speed) rather than an index position."},
      {"name":"Sorting algorithms", "q":"Why is merge sort preferred over quick sort sometimes?", "a":"Merge sort guarantees O(n log n) worst case. Quick sort can degrade to O(n²) with a bad pivot choice."},
      {"name":"Recursion + call stack", "q":"What is tail recursion?", "a":"When the recursive call is the absolute last operation. Note: standard Python doesn't optimise tail recursion."},
      {"name":"Backtracking", "q":"How to identify backtracking?", "a":"If the problem asks to 'generate all possible' permutations, combinations, or subsets. Try → recurse → undo."},
      {"name":"Dynamic programming", "q":"When is DP the right approach?", "a":"When you see overlapping subproblems + optimal substructure. If you draw a recursion tree and see repeated nodes, use DP."},
      {"name":"Greedy", "q":"How do you know greedy works vs DP?", "a":"Greedy works when making the local optimal choice leads to the global optimal solution. Prove it with an exchange argument."},
      {"name":"Graph algorithms", "q":"When does Dijkstra fail?", "a":"It fails when there are negative weight edges. You must use Bellman-Ford instead."},
      {"name":"Bit manipulation", "q":"XOR trick for finding a single duplicate?", "a":"Since a ^ a = 0, XOR all elements with 1..n. Everything cancels out except the duplicate."},
    ]
  },
  {
    "num": 5, "title": "Core CS Theory", "color": "#185FA5",
    "topics": [
      {"name":"OS — processes and threads", "q":"Process vs thread in one line?", "a":"A process has its own memory space, while threads share memory within the same process."},
      {"name":"OS — deadlock", "q":"4 conditions for deadlock?", "a":"Mutual exclusion, hold and wait, no preemption, and circular wait. All four must be true."},
      {"name":"OS — memory management", "q":"What is thrashing?", "a":"When a process spends more time paging (swapping memory to disk) than executing due to low RAM."},
      {"name":"DBMS — ER, normalisation", "q":"3NF vs BCNF?", "a":"3NF allows some redundancy for lossless joins. BCNF is stricter: every determinant must be a candidate key."},
      {"name":"DBMS — SQL deep dive", "q":"WHERE vs HAVING?", "a":"WHERE filters rows before grouping. HAVING filters after GROUP BY. You can't use aggregates in WHERE."},
      {"name":"DBMS — transactions", "q":"What is a dirty read?", "a":"When a transaction reads uncommitted data from another transaction. Prevented by 'Read Committed' isolation level."},
      {"name":"Computer networks", "q":"What layer does HTTP work at?", "a":"Application layer (Layer 7). TCP is Transport (Layer 4). IP is Network (Layer 3)."},
      {"name":"System design basics", "q":"Design a URL shortener flow", "a":"Hash function → 6-char code → store long:short in DB → redirect via lookup. Add caching for hot URLs."},
    ]
  },
  {
    "num": 6, "title": "Web Dev Gap-Fill", "color": "#854F0B",
    "topics": [
      {"name":"HTML/CSS + JS fundamentals", "q":"What is the event loop?", "a":"JS is single-threaded. The event loop picks tasks from the queue and executes them only when the call stack is empty."},
      {"name":"React hooks", "q":"useEffect vs useLayoutEffect?", "a":"useLayoutEffect fires synchronously before browser paint. useEffect fires asynchronously after paint. Default to useEffect."},
      {"name":"REST API design", "q":"PUT vs PATCH?", "a":"PUT replaces the entire resource. PATCH updates partial fields. Most APIs misuse PUT for partial updates."},
      {"name":"Git advanced", "q":"Rebase vs merge?", "a":"Rebase rewrites commit history for a clean linear log. Merge preserves history with a merge commit. Never rebase public branches."},
    ]
  },
  {
    "num": 7, "title": "AI/ML Track", "color": "#3B6D11",
    "topics": [
      {"name":"Math foundation", "q":"What is gradient descent?", "a":"Iteratively moving in the direction of steepest descent of a loss function to find the minimum. Step size = learning rate."},
      {"name":"Classical ML", "q":"Bias vs variance tradeoff?", "a":"High bias = underfitting (too simple). High variance = overfitting (too complex/noisy). Goal is to find the sweet spot."},
      {"name":"Evaluation metrics", "q":"When is F1 better than accuracy?", "a":"On imbalanced datasets. Accuracy is misleading when one class dominates. F1 balances precision and recall."},
      {"name":"Neural networks", "q":"Why ReLU over sigmoid?", "a":"Sigmoid suffers from vanishing gradients in deep networks. ReLU gradient is 1 for positive values, preventing vanishing."},
      {"name":"Transformers", "q":"What problem does attention solve?", "a":"RNNs forget long-range dependencies. Attention lets every token look at every other token simultaneously."},
      {"name":"RAG", "q":"RAG vs fine-tuning?", "a":"RAG injects knowledge at inference time (best for changing data). Fine-tuning changes model weights (best for format/style)."},
      {"name":"LLM agents", "q":"What is an LLM agent?", "a":"An LLM with access to external tools (like search/calc), capable of taking actions based on a reasoning loop (ReAct)."},
      {"name":"MLOps", "q":"What is model drift?", "a":"When a model's performance degrades over time because the real-world data distribution shifted away from the training data."},
    ]
  }
]

# 2. Build the Interview Q&A Page
qa_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Q&A Bank</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f1115;
            --surface-1: rgba(25, 27, 33, 0.6);
            --surface-2: rgba(35, 38, 47, 0.5);
            --border: rgba(255, 255, 255, 0.1);
            --text-1: #ffffff;
            --text-2: #a0a5b1;
            --brand: #ff5e00;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(255,94,0,0.1), transparent 40%),
                              radial-gradient(circle at bottom left, rgba(124,110,224,0.1), transparent 40%);
            color: var(--text-1);
            margin: 0; padding: 0; min-height: 100vh;
        }
        .container { max-width: 900px; margin: 4rem auto; padding: 0 1.5rem; }
        .hero { text-align: center; margin-bottom: 4rem; }
        .hero h1 { font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 1rem; }
        .hero p { font-size: 1.1rem; color: var(--text-2); max-width: 600px; margin: 0 auto; }
        
        .qa-block { margin-bottom: 3rem; }
        .block-title {
            font-size: 1.4rem; font-weight: 700; margin-bottom: 1.5rem; padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px;
        }
        
        .qa-card {
            background: var(--surface-1);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .qa-card:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.2); }
        .qa-q { font-size: 1.1rem; font-weight: 600; color: #fff; margin-bottom: 10px; display: flex; gap: 10px; align-items: flex-start;}
        .qa-q span { color: var(--brand); font-weight: 800; }
        .qa-a { font-size: 1rem; color: var(--text-2); line-height: 1.6; display: flex; gap: 10px; align-items: flex-start;}
        .qa-a span { color: #2ed573; font-weight: 800; }
        
        .back-btn {
            display: inline-flex; align-items: center; gap: 8px;
            color: var(--text-2); text-decoration: none; font-weight: 500;
            margin-bottom: 2rem; transition: color 0.2s;
        }
        .back-btn:hover { color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <a href="htmlfresher.html" class="back-btn">← Back to Tracker</a>
        <div class="hero">
            <h1>Interview Q&A Bank</h1>
            <p>Master these high-yield conceptual questions. How you answer these verbally dictates whether you pass the technical rounds.</p>
        </div>
"""
for b in blocks:
    qa_html += f"""
        <div class="qa-block">
            <div class="block-title" style="color: {b['color']}">{b['num']}. {b['title']}</div>"""
    for t in b["topics"]:
        if "q" in t and "a" in t:
            qa_html += f"""
            <div class="qa-card">
                <div class="qa-q"><span>Q.</span> {t['q']}</div>
                <div class="qa-a"><span>A.</span> {t['a']}</div>
            </div>"""
    qa_html += "</div>"
    
qa_html += """
    </div>
</body>
</html>
"""

with open(os.path.join(FRONTEND, "interview_qa.html"), "w") as f:
    f.write(qa_html)

# 3. Update Tracker & Notebook in htmlfresher.html
def update_frontend(html):
    # A. Remove topic-q-text and acc-badge
    html = re.sub(r'<span class="topic-q-text">.*?</span>', '', html, flags=re.DOTALL)
    html = re.sub(r'<span class=\'acc-badge\'>.*?</span>', '', html, flags=re.DOTALL)
    
    # B. Add "Interview Q&A Bank" button in the hero
    btn_html = """
    <a href="interview_qa.html" style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,94,0,0.15); border:1px solid rgba(255,94,0,0.3); color:#ff5e00; padding:8px 16px; border-radius:100px; text-decoration:none; font-weight:600; font-size:0.9rem; margin-top:12px; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,94,0,0.25)'" onmouseout="this.style.background='rgba(255,94,0,0.15)'">
        <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12l8.5 8.5"></path></svg>
        Interview Q&A Bank
    </a>"""
    
    # Insert button after the <p> in tracker-hero
    hero_pattern = r'(<div class="tracker-hero">.*?<p>.*?</p>)'
    if re.search(hero_pattern, html, flags=re.DOTALL):
        html = re.sub(hero_pattern, r'\1' + btn_html, html, flags=re.DOTALL, count=1)

    # C. Make Notebook Glassmorphism while keeping handwriting inside
    # Current css has .nb-master-container { background: var(--surface-1); }
    # We will change it to glass style:
    glass_css = """
.nb-master-container {
  display: flex; height: 820px;
  background: rgba(25, 27, 33, 0.4) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px !important;
  overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
  margin-top: 1.5rem;
}
.nb-sidebar {
  background: rgba(0,0,0,0.2) !important;
  border-right: 1px solid rgba(255,255,255,0.05) !important;
}
/* Ensure the page inside still looks like a notebook */
.notebook-paper {
  background-color: transparent !important; 
  /* The lines are still rendered, but background is transparent to show glass */
}
.nb-page-header { background-color: transparent !important; border-bottom: 2px solid rgba(255,255,255,0.1) !important; }
.nb-heading { border-bottom: 1px solid rgba(255,255,255,0.1) !important; }
"""
    
    # Insert this custom glass css before </style> of the notebook
    if '</style>' in html:
        # Find the last </style> to ensure we override
        idx = html.rfind('</style>')
        html = html[:idx] + glass_css + html[idx:]

    # D. Inject switchTab function so tabs actually work
    switchTab_js = """
<script>
function switchTab(tabId) {
    document.querySelectorAll('.nb-page').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nb-tab').forEach(el => el.classList.remove('active'));
    
    const page = document.getElementById('tab-' + tabId);
    if(page) page.classList.add('active');
    
    const tabs = document.querySelectorAll('.nb-tab');
    tabs.forEach(tab => {
        if(tab.getAttribute('onclick') && tab.getAttribute('onclick').includes(tabId)) {
            tab.classList.add('active');
        }
    });
}
</script>
"""
    # Insert script at the very end before closing body or just at the end
    if '</body>' in html:
        html = html.replace('</body>', switchTab_js + '\n</body>')
    else:
        html += switchTab_js

    return html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        new_content = update_frontend(content)
        with open(path, "w") as f:
            f.write(new_content)

print("V6 Updates Complete:")
print("- Removed Q&A from tracker rows")
print("- Removed 'cut from' badges")
print("- Created interview_qa.html with all Q&As")
print("- Added glassmorphism to Notebook while retaining handwriting font/lines")
print("- Fixed switchTab() function so tabs are clickable")
