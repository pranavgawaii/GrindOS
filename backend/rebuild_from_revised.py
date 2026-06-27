import os
import re
from datetime import datetime, timedelta

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# ── All 51 topics from grindos_revised_roadmap.html ───────────────────────
blocks = [
  {
    "num": 1, "title": "Python Foundation",
    "start": "Jun 26", "end": "Jul 03", "days": 7,
    "color": "#7C6EE0",
    "topics": [
      {"n":1, "name":"Variables, types, loops, conditionals", "sub":"if/else, for, while, type casting, input/output", "q":"\"What's the diff between a list and a tuple?\" → list mutable, tuple immutable", "due":"Jun 27"},
      {"n":2, "name":"Functions + scope + comprehensions", "sub":"*args, **kwargs, default args, lambda, map, filter, list comp", "q":"\"What is a closure?\" → function that remembers enclosing scope even after outer fn returns", "due":"Jun 28"},
      {"n":3, "name":"Data structures built-in", "sub":"List, tuple, set, dict — operations, methods, when each is right", "q":"\"When would you use a set over a list?\" → O(1) lookup, deduplication, membership test", "due":"Jun 29"},
      {"n":4, "name":"Strings + file handling + exceptions", "sub":"slicing, f-strings, open/read/write, try/except/finally, context manager", "q":"\"What does 'with open()' do differently?\" → context manager auto-closes file, even on error", "due":"Jun 30"},
      {"n":5, "name":"Modules, stdlib, decorators intro", "sub":"os, sys, datetime, collections, @property basics", "q":"\"What is a decorator?\" → function that wraps another function to modify behaviour", "due":"Jul 01"},
      {"n":6, "name":"Mini project: build banking system", "sub":"Account class, deposit/withdraw, balance check — no OOP yet, pure Python functions", "q":"This is your revision checkpoint. If you can build it, you know block 1.", "due":"Jul 03"},
    ]
  },
  {
    "num": 2, "title": "Object Oriented Programming",
    "start": "Jul 03", "end": "Jul 09", "days": 6,
    "color": "#0F6E56",
    "badge": "cut from 15 days",
    "topics": [
      {"n":7, "name":"Classes, objects, __init__, self", "sub":"Rebuild banking system with classes now", "q":"\"What is self?\" → reference to current instance, Python doesn't pass it implicitly like Java's this", "due":"Jul 04"},
      {"n":8, "name":"Encapsulation + inheritance", "sub":"private attrs, @property, single/multiple/multilevel, MRO, super()", "q":"\"What is MRO?\" → C3 linearisation, determines which parent method is called. Check with ClassName.__mro__", "due":"Jul 05"},
      {"n":9, "name":"Polymorphism + abstraction", "sub":"method overriding, duck typing, ABC module, abstract methods", "q":"\"Abstraction vs encapsulation?\" → encapsulation = HOW you hide (bundling). Abstraction = WHAT you hide (interface).", "due":"Jul 06"},
      {"n":10, "name":"Dunder methods + class/static methods", "sub":"__str__, __repr__, __len__, __eq__, @classmethod, @staticmethod", "q":"\"When use @staticmethod vs @classmethod?\" → static = no access to class/instance. classmethod gets cls, useful for factory methods.", "due":"Jul 07"},
      {"n":11, "name":"Decorators deep dive", "sub":"Write your own decorator, @wraps, chaining decorators", "q":"\"What is a decorator really?\" → it's syntactic sugar. @dec def f() is the same as f = dec(f)", "due":"Jul 08"},
      {"n":12, "name":"OOP checkpoint — upgrade banking system", "sub":"Add SavingsAccount (inheritance), abstract Account base, __str__ for display", "q":"If you can build this from memory — you're done with OOP. Don't spend more days here.", "due":"Jul 09"},
    ]
  },
  {
    "num": 3, "title": "Data Structures (implement from scratch)",
    "start": "Jul 09", "end": "Jul 25", "days": 16,
    "color": "#993C1D",
    "topics": [
      {"n":13, "name":"Arrays + strings", "sub":"in-place ops, string immutability, two-pointer intro, pattern matching", "q":"\"Why is string concatenation O(n²) in a loop?\" → each + creates new string. Use join() instead.", "due":"Jul 11"},
      {"n":14, "name":"Stack + queue", "sub":"LIFO/FIFO, implement both using list and deque, circular queue, bracket matching", "q":"\"When do you use a stack?\" → undo/redo, expression evaluation, DFS, backtracking", "due":"Jul 13"},
      {"n":15, "name":"Linked list (implement fully)", "sub":"Node class, singly + doubly, insert/delete/reverse from scratch", "q":"\"How detect a cycle in linked list?\" → Floyd's tortoise and hare. Fast and slow pointer meet if cycle exists.", "due":"Jul 15"},
      {"n":16, "name":"HashMap + set", "sub":"collision handling, chaining vs open addressing, O(1) amortised, set operations", "q":"\"When does O(1) break for HashMap?\" → hash collision makes worst case O(n). Python dict uses open addressing.", "due":"Jul 17"},
      {"n":17, "name":"Binary tree + BST", "sub":"TreeNode class, inorder/preorder/postorder, height, diameter, BST insert/delete/validate", "q":"\"What makes a valid BST?\" → all left < node < all right. Not just immediate children — ALL descendants.", "due":"Jul 20"},
      {"n":18, "name":"Heap + priority queue", "sub":"min-heap, max-heap, heapq module, heappush/heappop, top-K pattern", "q":"\"How to get K largest elements efficiently?\" → min-heap of size K. O(n log K) vs O(n log n) sort.", "due":"Jul 22"},
      {"n":19, "name":"Graphs (BFS + DFS implement both)", "sub":"adjacency list, adjacency matrix, BFS (queue), DFS (stack/recursion), cycle detection", "q":"\"BFS vs DFS — when to use which?\" → BFS = shortest path in unweighted graph. DFS = detect cycle, topological sort, maze solving.", "due":"Jul 24"},
      {"n":20, "name":"Trie", "sub":"TrieNode class, insert + search + startsWith from scratch", "q":"\"Why use a Trie over HashMap for prefix search?\" → Trie gives prefix matching natively. HashMap needs scanning all keys.", "due":"Jul 25"},
    ]
  },
  {
    "num": 4, "title": "DSA Problem Patterns (the real grind)",
    "start": "Jul 25", "end": "Aug 18", "days": 24,
    "color": "#A32D2D",
    "badge": "expanded from 15 days",
    "topics": [
      {"n":21, "name":"Two pointers", "sub":"pair sum, remove duplicates, container with most water, 3Sum", "q":"Pattern: sorted array or need to find pair/triplet — default to two pointers first", "due":"Jul 27"},
      {"n":22, "name":"Sliding window", "sub":"max sum subarray, longest substring no repeat, minimum window substring", "q":"Pattern: contiguous subarray/substring problem → sliding window. Fixed vs variable window.", "due":"Jul 29"},
      {"n":23, "name":"Binary search", "sub":"classic, search rotated array, first/last position, binary search on answer", "q":"\"When to use binary search on the answer?\" → when you're searching for a minimum/maximum value, not a position", "due":"Jul 31"},
      {"n":24, "name":"Sorting algorithms", "sub":"Merge sort + quick sort — write both from scratch. Know time complexity proof.", "q":"\"Why is merge sort preferred over quick sort?\" → merge sort O(n log n) worst case. Quick sort O(n²) worst case (bad pivot).", "due":"Aug 02"},
      {"n":25, "name":"Recursion + call stack", "sub":"base case, recursion tree, factorial, fibonacci, print all paths", "q":"\"What is tail recursion?\" → recursive call is last operation. Python doesn't optimise it unlike some other languages.", "due":"Aug 04"},
      {"n":26, "name":"Backtracking", "sub":"permutations, combinations, subsets, N-Queens — understand prune + explore pattern", "q":"Pattern: \"generate all possible...\" → backtracking. Try → recurse → undo.", "due":"Aug 07"},
      {"n":27, "name":"Dynamic programming — basics", "sub":"memorization (top-down) vs tabulation (bottom-up), Fibonacci DP, climbing stairs, house robber", "q":"\"When is DP the right approach?\" → overlapping subproblems + optimal substructure. If you see recursion with repeated calls — DP it.", "due":"Aug 10"},
      {"n":28, "name":"DP patterns — knapsack + sequences", "sub":"0/1 knapsack, coin change, LCS, LIS, matrix chain, edit distance", "q":"These 6 cover 80% of DP interview problems. Master coin change first — it unlocks knapsack intuition.", "due":"Aug 13"},
      {"n":29, "name":"Greedy", "sub":"activity selection, interval scheduling, fractional knapsack, Huffman", "q":"\"How do you know greedy works vs DP?\" → greedy works when local optimal = global optimal. Prove it with exchange argument.", "due":"Aug 15"},
      {"n":30, "name":"Graph algorithms", "sub":"Dijkstra, topological sort, union-find, Kruskal/Prim (MST basics)", "q":"\"When does Dijkstra fail?\" → negative weight edges. Use Bellman-Ford instead.", "due":"Aug 17"},
      {"n":31, "name":"Bit manipulation + math", "sub":"XOR tricks, count set bits, subsets, GCD/LCM, prime sieve, modular arithmetic", "q":"\"XOR trick for finding duplicate?\" → a XOR a = 0. XOR all elements + 1..n → the duplicate remains.", "due":"Aug 18"},
    ]
  },
  {
    "num": 5, "title": "Core CS Theory — OS, DBMS, CN, System Design",
    "start": "Aug 18", "end": "Sep 01", "days": 14,
    "color": "#185FA5",
    "topics": [
      {"n":32, "name":"OS — processes and threads", "sub":"process vs thread, PCB, context switching, CPU scheduling (FCFS, SJF, Round Robin)", "q":"\"Process vs thread in one line?\" → process has its own memory, threads share memory within a process", "due":"Aug 20"},
      {"n":33, "name":"OS — deadlock + synchronisation", "sub":"4 conditions, banker's algorithm, semaphore, mutex, race condition", "q":"\"4 conditions for deadlock?\" → mutual exclusion, hold and wait, no preemption, circular wait", "due":"Aug 22"},
      {"n":34, "name":"OS — memory management", "sub":"paging, segmentation, virtual memory, page replacement (LRU, FIFO, optimal)", "q":"\"What is thrashing?\" → process spends more time paging than executing. Too many processes, too little RAM.", "due":"Aug 24"},
      {"n":35, "name":"DBMS — ER, normalisation", "sub":"ER diagrams, 1NF/2NF/3NF/BCNF with examples, functional dependency", "q":"\"3NF vs BCNF?\" → 3NF allows some redundancy for lossless join. BCNF is stricter, every determinant is a candidate key.", "due":"Aug 26"},
      {"n":36, "name":"DBMS — SQL deep dive", "sub":"JOINs, GROUP BY, HAVING, window functions, indexes (clustered vs non-clustered)", "q":"\"WHERE vs HAVING?\" → WHERE filters rows before grouping. HAVING filters after GROUP BY. Can't use aggregate in WHERE.", "due":"Aug 28"},
      {"n":37, "name":"DBMS — transactions, ACID, stored procs", "sub":"ACID properties, isolation levels, transactions, triggers, views", "q":"\"What is a dirty read?\" → transaction reads uncommitted data from another transaction. Prevented by isolation level Read Committed.", "due":"Aug 29"},
      {"n":38, "name":"Computer networks — OSI + protocols", "sub":"OSI 7 layers, TCP vs UDP, TCP 3-way handshake, HTTP/HTTPS, DNS, IP", "q":"\"What layer does HTTP work at?\" → Application layer (Layer 7). TCP is Transport (Layer 4). IP is Network (Layer 3).", "due":"Aug 31"},
      {"n":39, "name":"System design basics", "sub":"client-server, monolith vs microservices, load balancing, caching (Redis), message queues, URL shortener design", "q":"\"Design a URL shortener\" → hash function → 6-char code → store long:short in DB → redirect via lookup. Add caching for hot URLs.", "due":"Sep 01"},
    ]
  },
  {
    "num": 6, "title": "Web Dev Gap-Fill (you already know most of this)",
    "start": "Sep 01", "end": "Sep 05", "days": 4,
    "color": "#854F0B",
    "badge": "cut from 5 days",
    "topics": [
      {"n":40, "name":"HTML/CSS + JS fundamentals", "sub":"box model, flexbox, closures, event loop, promises, async/await — verbal fluency only", "q":"\"What is the event loop?\" → JS is single-threaded. Event loop picks tasks from queue and executes when call stack is empty.", "due":"Sep 02"},
      {"n":41, "name":"React hooks + Next.js patterns", "sub":"useEffect, useCallback, useMemo, SSR vs SSG vs ISR — you've built with this, just articulate it", "q":"\"useEffect vs useLayoutEffect?\" → useLayoutEffect fires before browser paints. useEffect fires after. Default to useEffect.", "due":"Sep 03"},
      {"n":42, "name":"REST API design + backend patterns", "sub":"HTTP methods, status codes, middleware, auth patterns (JWT, OAuth) — you built this in Auren", "q":"\"PUT vs PATCH?\" → PUT replaces entire resource. PATCH updates partial fields.", "due":"Sep 04"},
      {"n":43, "name":"Git advanced + deployment", "sub":"rebase vs merge, squash, cherry-pick, Vercel/Railway env vars, CI/CD basics", "q":"\"Rebase vs merge?\" → rebase rewrites commit history for cleaner log. Merge preserves history with a merge commit. Never rebase public branches.", "due":"Sep 05"},
    ]
  },
  {
    "num": 7, "title": "AI/ML Track (you have a head start here)",
    "start": "Sep 05", "end": "Sep 12", "days": 7,
    "color": "#3B6D11",
    "badge": "cut from 10 days",
    "topics": [
      {"n":44, "name":"Math foundation — verbal only", "sub":"gradient intuition, Bayes theorem, variance, covariance — no deep calc, just explain clearly", "q":"\"What is gradient descent?\" → iteratively move in direction of steepest descent of loss function. Step size = learning rate.", "due":"Sep 06"},
      {"n":45, "name":"Classical ML algorithms", "sub":"Linear Reg, Logistic Reg, Decision Tree, Random Forest, SVM, KNN, K-Means, Naive Bayes", "q":"\"Bias vs variance tradeoff?\" → high bias = underfitting (too simple). High variance = overfitting (too complex).", "due":"Sep 07"},
      {"n":46, "name":"Evaluation metrics", "sub":"accuracy, precision, recall, F1, ROC-AUC, confusion matrix — when to use each", "q":"\"When is F1 better than accuracy?\" → imbalanced dataset. Accuracy is misleading when one class dominates.", "due":"Sep 07"},
      {"n":47, "name":"Neural networks + backprop", "sub":"feedforward, activations (ReLU/sigmoid/softmax), loss functions, optimisers, dropout, batch norm", "q":"\"Why ReLU over sigmoid?\" → sigmoid has vanishing gradient problem for deep networks. ReLU gradient is 1 for positive values.", "due":"Sep 08"},
      {"n":48, "name":"Transformers + attention mechanism", "sub":"self-attention, multi-head attention, positional encoding, BERT vs GPT, encoder vs decoder", "q":"\"What problem does attention solve?\" → RNNs forget long-range dependencies. Attention lets every token attend to every other token at once.", "due":"Sep 09"},
      {"n":49, "name":"RAG + vector DBs + embeddings", "sub":"RAG pipeline, pgvector, cosine similarity, HNSW — you built this in Mnemo, just articulate it clearly", "q":"\"RAG vs fine-tuning?\" → RAG = inject knowledge at inference time. Fine-tuning = change model weights.", "due":"Sep 10"},
      {"n":50, "name":"LLM agents + prompt engineering", "sub":"tool calling, ReAct pattern, zero/few-shot, chain-of-thought, LangGraph basics", "q":"\"What is an LLM agent?\" → LLM with access to tools, can take actions based on reasoning loop. You built this in Auren — say that.", "due":"Sep 11"},
      {"n":51, "name":"MLOps basics", "sub":"training pipeline, FastAPI inference, model drift, Docker containerisation", "q":"\"What is model drift?\" → model performance degrades because real-world data distribution shifts from training data over time.", "due":"Sep 12"},
    ]
  },
]

total_topics = sum(len(b["topics"]) for b in blocks)

# ── Build Tracker HTML ─────────────────────────────────────────────────────
tracker_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&display=swap');

/* Metrics Matrix */
.metrics-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:2.5rem;}
.metric-box{background:var(--surface-1);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1rem;display:flex;flex-direction:column;gap:4px;position:relative;overflow:hidden;}
.metric-box::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--border-strong);}
.overdue-box::after{background:#ff4757;}
.metric-val{font-size:2rem;font-weight:800;color:var(--text-1);line-height:1;}
.metric-lbl{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-muted);font-weight:600;}
.overdue-val{color:#ff4757!important;}
.days-left-val{color:var(--brand)!important;}

/* Tracker Container */
.checklist-master-container{max-width:900px;margin:0 auto;padding:0 1rem 120px;}
.tracker-hero{margin-bottom:2rem;}
.tracker-hero h1{font-size:1.8rem;font-weight:800;color:var(--text-1);}
.tracker-hero p{font-size:0.9rem;color:var(--text-3);margin-top:4px;}

/* Accordion */
.acc-card{background:var(--surface-1);border:1px solid var(--border);border-radius:12px;margin-bottom:1rem;overflow:hidden;transition:border-color .2s;box-shadow:0 2px 12px rgba(0,0,0,0.08);}
.acc-card:hover{border-color:var(--border-strong);}
.acc-header{padding:1rem 1.25rem;background:var(--surface-2);display:flex;align-items:center;gap:14px;cursor:pointer;user-select:none;}
.acc-block-num{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:800;color:#fff;flex-shrink:0;}
.acc-header-info{flex:1;display:flex;flex-direction:column;gap:3px;align-items:flex-start;}
.acc-title{font-size:0.92rem;font-weight:700;color:var(--text-1);text-align:left;text-transform:uppercase;letter-spacing:0.04em;}
.acc-meta-row{display:flex;align-items:center;gap:10px;}
.acc-date-info{font-size:0.75rem;color:var(--text-3);font-weight:500;}
.acc-badge{font-size:0.68rem;padding:2px 7px;border-radius:10px;background:rgba(245,166,35,0.15);color:#b87d00;border:1px solid rgba(245,166,35,0.2);font-weight:600;}
.acc-chevron{flex-shrink:0;color:var(--text-3);transition:transform .25s;}
.acc-card.open .acc-chevron{transform:rotate(180deg);}
.acc-body{display:none;border-top:1px solid var(--border);}
.acc-card.open .acc-body{display:block;}

/* Topic Rows */
.topic-rows{display:flex;flex-direction:column;}
.topic-row-item{display:grid;grid-template-columns:36px 1fr auto;gap:12px;align-items:start;padding:0.85rem 1.25rem;border-bottom:1px solid var(--border-light);cursor:pointer;transition:background .15s;}
.topic-row-item:last-child{border-bottom:none;}
.topic-row-item:hover{background:var(--surface-0);}
.topic-row-item.checked{opacity:0.6;}
.topic-check-area{display:flex;align-items:center;justify-content:center;padding-top:2px;}
.topic-checkbox{display:none;}
.topic-check-box{width:20px;height:20px;border-radius:5px;border:2px solid var(--text-4);display:flex;align-items:center;justify-content:center;transition:all .15s;flex-shrink:0;}
.topic-checkbox:checked + .topic-check-box{background:var(--text-1);border-color:var(--text-1);}
.topic-checkbox:checked + .topic-check-box::after{content:'✓';color:var(--bg);font-size:13px;font-weight:800;}
.topic-body{display:flex;flex-direction:column;gap:3px;text-align:left;}
.topic-name{font-size:0.9rem;font-weight:600;color:var(--text-1);text-align:left;line-height:1.4;}
.topic-checkbox:checked ~ .topic-body .topic-name{text-decoration:line-through;color:var(--text-4);}
.topic-sub-text{font-size:0.8rem;color:var(--text-3);line-height:1.5;text-align:left;}
.topic-q-text{font-size:0.78rem;color:var(--brand);margin-top:4px;line-height:1.5;text-align:left;font-style:italic;}
.topic-meta{display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
.topic-num-badge{font-size:0.72rem;color:var(--text-muted);font-weight:700;}
.topic-due{font-size:0.72rem;font-weight:600;padding:2px 8px;border-radius:10px;white-space:nowrap;}
.due-normal{color:var(--text-muted);background:var(--surface-0);border:1px solid var(--border);}
.due-overdue{color:#ff4757;background:rgba(255,71,87,.1);border:1px solid rgba(255,71,87,.25);}

/* Floating Pill */
.fp-pill{position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);background:var(--surface-2);border:1px solid var(--border-strong);border-radius:100px;padding:12px 28px;display:flex;align-items:center;width:90%;max-width:500px;box-shadow:0 8px 30px rgba(0,0,0,.35);z-index:1000;backdrop-filter:blur(12px);}
.fp-info{flex:1;}
.fp-row{display:flex;justify-content:space-between;font-size:.82rem;font-weight:600;color:var(--text-2);margin-bottom:6px;}
.fp-track{height:6px;background:var(--surface-0);border-radius:3px;overflow:hidden;}
.fp-fill{height:100%;background:var(--text-1);border-radius:3px;width:0%;transition:width .3s;}
</style>"""

blocks_html = ""
for block in blocks:
    topics_html = ""
    for t in block["topics"]:
        due_disp = t["due"]
        # parse due date for overdue logic - we embed the date as data attr
        # Convert "Jun 27" to "2026-06-27" etc.
        months = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
        parts = due_disp.split()
        if len(parts) == 2:
            m, d = parts
            due_iso = f"2026-{months.get(m,'01')}-{d.zfill(2)}"
        else:
            due_iso = "2026-12-31"

        topics_html += f"""
        <label class="topic-row-item" onclick="event.stopPropagation()">
          <div class="topic-check-area">
            <input type="checkbox" class="topic-checkbox" id="t-{t['n']}" data-due="{due_iso}">
            <div class="topic-check-box"></div>
          </div>
          <div class="topic-body">
            <span class="topic-name">{t['name']}</span>
            <span class="topic-sub-text">{t['sub']}</span>
            <span class="topic-q-text">Q: {t['q']}</span>
          </div>
          <div class="topic-meta">
            <span class="topic-num-badge">#{t['n']}</span>
            <span class="topic-due due-normal" id="badge-{t['n']}">{due_disp}</span>
          </div>
        </label>"""

    badge_html = f"<span class='acc-badge'>{block.get('badge','')}</span>" if block.get('badge') else ""
    blocks_html += f"""
    <div class="acc-card" onclick="toggleAcc(this)">
      <div class="acc-header">
        <div class="acc-block-num" style="background:{block['color']}">{block['num']}</div>
        <div class="acc-header-info">
          <span class="acc-title">{block['title']}</span>
          <div class="acc-meta-row">
            <span class="acc-date-info">{block['start']} → {block['end']} · {block['days']} days</span>
            {badge_html}
          </div>
        </div>
        <div class="acc-chevron">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>
      <div class="acc-body">
        <div class="topic-rows">{topics_html}</div>
      </div>
    </div>"""

new_tracker = f"""{tracker_css}
<div class="checklist-master-container" id="checklist-master">
  <div class="tracker-hero">
    <h1>Roadmap Tracker</h1>
    <p>51 topics · Revised plan · Grind ends Sep 12, 2026 · 12-day mock buffer</p>
  </div>
  <div class="metrics-grid">
    <div class="metric-box">
      <span class="metric-val" id="m-total">{total_topics}</span>
      <span class="metric-lbl">Total Topics</span>
    </div>
    <div class="metric-box">
      <span class="metric-val" id="m-done">0</span>
      <span class="metric-lbl">Completed</span>
    </div>
    <div class="metric-box">
      <span class="metric-val days-left-val" id="m-days">78</span>
      <span class="metric-lbl">Days to Sep 12</span>
    </div>
    <div class="metric-box overdue-box">
      <span class="metric-val overdue-val" id="m-overdue">0</span>
      <span class="metric-lbl">Overdue ⚠</span>
    </div>
  </div>
  <div>{blocks_html}</div>
</div>
<div class="fp-pill">
  <div class="fp-info">
    <div class="fp-row"><span>Overall Mastery</span><span id="fp-pct">0%</span></div>
    <div class="fp-track"><div class="fp-fill" id="fp-bar"></div></div>
  </div>
</div>
<script>
function toggleAcc(el) {{ el.classList.toggle('open'); }}
function syncProgress() {{
  const all = document.querySelectorAll('.topic-checkbox');
  const today = new Date(); today.setHours(0,0,0,0);
  let done = 0, overdue = 0;
  all.forEach(cb => {{
    const checked = cb.checked;
    if (checked) done++;
    const due = cb.getAttribute('data-due');
    const num = cb.id.split('-')[1];
    const badge = document.getElementById('badge-' + num);
    if (badge && due) {{
      const d = new Date(due);
      if (!checked && d < today) {{
        overdue++;
        badge.className = 'topic-due due-overdue';
        badge.textContent = 'Overdue!';
      }} else {{
        badge.className = 'topic-due due-normal';
        badge.textContent = d.toLocaleDateString('en-US', {{month:'short', day:'numeric'}});
      }}
    }}
  }});
  document.getElementById('m-done').textContent = done;
  // Days to Sep 12
  const end = new Date('2026-09-12'); const now = new Date(); now.setHours(0,0,0,0);
  const dLeft = Math.max(0, Math.ceil((end - now) / 86400000));
  document.getElementById('m-days').textContent = dLeft;
  document.getElementById('m-overdue').textContent = overdue;
  const pct = all.length ? Math.round(done/all.length*100) : 0;
  document.getElementById('fp-pct').textContent = pct + '%';
  document.getElementById('fp-bar').style.width = pct + '%';
}}
document.querySelectorAll('.topic-checkbox').forEach(cb => {{
  const saved = localStorage.getItem('grindos-r-' + cb.id);
  if (saved === '1') cb.checked = true;
  cb.addEventListener('change', e => {{
    localStorage.setItem('grindos-r-' + cb.id, e.target.checked ? '1' : '0');
    syncProgress();
  }});
}});
window.addEventListener('DOMContentLoaded', syncProgress);
</script>"""

# ── Build Notebook CSS (handwriting font, proper box) ─────────────────────
notebook_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&display=swap');

/* Notebook Container */
.nb-master-container {
  display: flex;
  height: 820px;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  background: var(--surface-1);
  box-shadow: 0 8px 40px rgba(0,0,0,.12);
  margin-top: 1.5rem;
}
.nb-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--surface-2);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
}
.nb-sidebar-head {
  padding: 1.25rem 1rem 1rem;
  border-bottom: 1px solid var(--border);
}
.nb-sidebar-head h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-1);
  margin: 0 0 3px;
}
.nb-sidebar-head small {
  font-size: 0.72rem;
  color: var(--text-muted);
}
.nb-tabs-v {
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
  flex: 1;
}
.nb-tab {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-2);
  transition: all .15s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}
.nb-tab:hover { background: var(--surface-0); color: var(--text-1); }
.nb-tab.active { background: rgba(255,94,0,.1); color: var(--brand); font-weight: 600; }

/* Content Pane */
.nb-content-pane {
  flex: 1;
  overflow-y: auto;
  background: var(--bg);
  position: relative;
}
.nb-page { display: none; height: 100%; }
.nb-page.active { display: block; animation: nbIn .2s ease; }
@keyframes nbIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none} }

/* Notebook Paper Style */
.notebook-paper {
  min-height: 100%;
  background: var(--bg);
  background-image:
    linear-gradient(var(--border-light) 1px, transparent 1px);
  background-size: 100% 36px;
  background-position: 0 52px;
  padding: 0;
  position: relative;
}
.notebook-paper::before {
  content: '';
  position: absolute;
  left: 68px;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(255, 100, 100, 0.25);
}

/* Page Header */
.nb-page-header {
  padding: 1.25rem 1.5rem 0.75rem 5rem;
  border-bottom: 2px solid var(--border);
  margin-bottom: 0;
  background: var(--bg);
}
.nb-page-subject {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--brand);
  font-weight: 700;
  margin-bottom: 4px;
}
.nb-page-title {
  font-family: 'Caveat', cursive;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-1);
  line-height: 1.2;
}

/* Content Lines */
.nb-lines {
  padding: 1rem 1.5rem 2rem 5rem;
}
.nb-line {
  font-family: 'Caveat', cursive;
  font-size: 1.25rem;
  line-height: 2.25rem;
  color: var(--text-1);
  display: block;
  min-height: 36px;
}
.nb-blank { min-height: 36px; display: block; }
.nb-heading {
  font-family: 'Caveat', cursive;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-1);
  line-height: 2.25rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
  display: block;
}
.nb-sub {
  font-family: 'Caveat', cursive;
  font-size: 1.15rem;
  color: var(--text-2);
  line-height: 2.25rem;
  padding-left: 1.5rem;
  display: block;
}
.nb-arrow { color: var(--brand); margin-right: 6px; font-weight: 700; }
.nb-trap {
  font-family: 'Caveat', cursive;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff4757;
  line-height: 2.25rem;
  display: block;
}
.nb-note {
  font-family: 'Caveat', cursive;
  font-size: 1.1rem;
  color: var(--brand);
  line-height: 2.25rem;
  display: block;
  padding-left: 1.5rem;
  border-left: 3px solid rgba(255,94,0,0.3);
  margin: 4px 0;
}

/* Sticky Note */
.nb-sticky {
  background: rgba(255, 220, 100, 0.15);
  border: 1px solid rgba(255, 200, 50, 0.3);
  border-radius: 0 8px 8px 0;
  border-left: 4px solid rgba(255, 200, 50, 0.6);
  padding: 0.75rem 1rem;
  margin: 1rem 1.5rem 1rem 4.5rem;
  font-family: 'Caveat', cursive;
  font-size: 1.15rem;
  color: var(--text-1);
  line-height: 1.7;
}
.nb-sticky-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #b87d00;
  font-weight: 700;
  margin-bottom: 4px;
  font-family: system-ui, sans-serif;
}
</style>"""

# Extract real notebook page content from the source HTML
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_src = f.read()

def extract_nb_page(src, tab_id):
    pat = rf'<div id="tab-{tab_id}" class="nb-page[^"]*">(.*?)(?=<div id="tab-|\Z)'
    m = re.search(pat, src, flags=re.DOTALL)
    if m:
        return m.group(1).strip()
    return "<p>Content not found.</p>"

# Convert old ruled-paper markup to new notebook-paper markup
def convert_to_notebook_style(old_html, subject, title, day):
    # Extract the ruled lines content
    ruled_match = re.search(r'<div class="ruled">(.*?)</div>\s*(?:<div class="sticky"|</div>)', old_html, flags=re.DOTALL)
    lines_html = ""
    if ruled_match:
        ruled_content = ruled_match.group(1)
        # Convert each line
        line_parts = re.findall(r'<span class="line-content[^"]*">(.*?)</span>', ruled_content, flags=re.DOTALL)
        for lc in line_parts:
            # Remove HTML tags to get text
            text = re.sub(r'<[^>]+>', '', lc).strip()
            if not text:
                lines_html += "<span class='nb-blank'></span>\n"
                continue
            # Detect heading-like spans
            if re.search(r'class="hl-', lc):
                lines_html += f"<span class='nb-heading'>{text}</span>\n"
            elif "INTERVIEW TRAP" in text or "TRAP:" in text:
                lines_html += f"<span class='nb-trap'>⚡ {text}</span>\n"
            elif re.search(r'class="arrow"', lc) or text.startswith('→'):
                lines_html += f"<span class='nb-sub'><span class='nb-arrow'>→</span>{text.lstrip('→').strip()}</span>\n"
            elif re.search(r'class="indent"', lc):
                lines_html += f"<span class='nb-sub'>{text}</span>\n"
            elif text.startswith('MY EXAMPLE') or text.startswith('NOTE:'):
                lines_html += f"<span class='nb-note'>{text}</span>\n"
            else:
                lines_html += f"<span class='nb-line'>{text}</span>\n"

    # Get sticky content
    sticky_match = re.search(r'<div class="sticky">(.*?)</div>', old_html, flags=re.DOTALL)
    sticky_html = ""
    if sticky_match:
        sticky_content = sticky_match.group(1)
        sticky_title_m = re.search(r'<div class="sticky-title">(.*?)</div>', sticky_content)
        sticky_p_m = re.search(r'<p>(.*?)</p>', sticky_content, flags=re.DOTALL)
        if sticky_title_m or sticky_p_m:
            st = re.sub(r'<[^>]+>', '', sticky_title_m.group(1) if sticky_title_m else "Remember").strip()
            sp = re.sub(r'<[^>]+>', '', sticky_p_m.group(1) if sticky_p_m else "").strip()
            sticky_html = f"""
            <div class="nb-sticky">
                <div class="nb-sticky-label">{st}</div>
                {sp}
            </div>"""

    return f"""
    <div class="notebook-paper">
        <div class="nb-page-header">
            <div class="nb-page-subject">{subject}</div>
            <div class="nb-page-title">{title}</div>
        </div>
        <div class="nb-lines">
            {lines_html}
        </div>
        {sticky_html}
    </div>"""

keep_tabs = [
    ("os",       "Core CS · OS",      "Deadlock — my one-pager",           "Day 33",  "📋"),
    ("dbms",     "Core CS · DBMS",    "SQL + Joins — my one-pager",        "Day 36",  "🗃️"),
    ("tips",     "Interview Prep",    "Tips, tricks & what not to do",     "Day 50",  "💡"),
    ("playbook", "Fresher Playbook",  "Everything in one place",           "Day 51",  "📖"),
]

sidebar_items = ""
pages_html = ""
for i, (tid, subj, title, day, icon) in enumerate(keep_tabs):
    active = " active" if i == 0 else ""
    sidebar_items += f"""
        <div class="nb-tab{active}" onclick="switchTab('{tid}')">
          <span style="font-size:1.1rem">{icon}</span> {title.split(' —')[0]}
        </div>"""
    raw = extract_nb_page(nb_src, tid)
    converted = convert_to_notebook_style(raw, subj, title, day)
    pages_html += f'<div id="tab-{tid}" class="nb-page{active}">{converted}</div>\n'

new_notebook = f"""{notebook_css}
<div class="nb-master-container">
  <div class="nb-sidebar">
    <div class="nb-sidebar-head">
      <h3>Interview Notes</h3>
      <small>Only what you need to pass</small>
    </div>
    <div class="nb-tabs-v">
      {sidebar_items}
    </div>
  </div>
  <div class="nb-content-pane">
    {pages_html}
  </div>
</div>"""

# ── Apply to HTML files ────────────────────────────────────────────────────
for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if not os.path.exists(path):
        continue
    with open(path, "r") as f:
        html = f.read()

    # Replace tracker
    t_start = html.find('<div class="checklist-master-container"')
    if t_start != -1:
        t_end = html.find('</script>', t_start) + len('</script>')
        # Find the CSS block before it
        css_start = html.rfind('<style>', 0, t_start)
        if css_start != -1:
            html = html[:css_start] + new_tracker + html[t_end:]
        else:
            html = html[:t_start] + new_tracker + html[t_end:]
        print(f"  ✓ Tracker replaced in {filename}")

    # Replace notebook
    nb_start = html.find('<div class="nb-master-container">')
    if nb_start != -1:
        # Find the CSS before it
        css_start = html.rfind('<style>', 0, nb_start)
        if css_start != -1:
            nb_css_start = css_start
        else:
            nb_css_start = nb_start
        # Find the end - the switchTab script
        nb_end = html.find('function switchTab', nb_start)
        if nb_end != -1:
            end_script = html.find('</script>', nb_end) + len('</script>')
            html = html[:nb_css_start] + new_notebook + html[end_script:]
            print(f"  ✓ Notebook replaced in {filename}")
        else:
            # depth match
            depth = 0
            idx = nb_start
            while idx < len(html):
                if html[idx:idx+4] == '<div': depth += 1
                elif html[idx:idx+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        html = html[:nb_css_start] + new_notebook + html[idx+6:]
                        print(f"  ✓ Notebook replaced (depth) in {filename}")
                        break
                idx += 1
    else:
        print(f"  ✗ Could not find notebook in {filename}")

    with open(path, "w") as f:
        f.write(html)

print(f"\n✓ Done! {total_topics} topics from revised roadmap loaded. Notebook handwriting style applied.")
