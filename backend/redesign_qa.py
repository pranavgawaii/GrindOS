import os
import re

file_path = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/interview_qa.html"
with open(file_path, 'r') as f:
    content = f.read()

# Parse the cards
cards = re.findall(r'<div class="qa-card">(.*?)</div>\s*</div>' if False else r'<div class="qa-card">(.*?)</div>\s*(?=<div class="qa-card">|</div>\s*</div>)', content, re.DOTALL)

# Re-parse more robustly
cards_html = re.search(r'<div class="qa-grid">(.*?)</div>\s*</div>\s*<script>', content, re.DOTALL)
if cards_html:
    grid_content = cards_html.group(1)
    card_matches = re.findall(r'<div class="qa-card">(.*?)</div>\s*(?=<div class="qa-card">|$)', grid_content, re.DOTALL)
else:
    print("Could not find qa-grid")
    exit(1)

parsed_cards = []
for card in card_matches:
    q = re.search(r'<div class="qa-q"><span class="qa-q-icon">.*?</span>\s*(.*?)</div>', card).group(1)
    a = re.search(r'<div class="qa-a">(.*?)</div>', card).group(1)
    strat = re.search(r'<b>Premium Strategy</b>\s*(.*?)\s*</div>', card).group(1)
    
    # Very simple categorisation based on keywords
    if any(k in q.lower() for k in ['python', 'list', 'tuple', 'closure', 'set', 'with open', 'decorator', 'self', 'mro', 'static', 'string']):
        cat = "Python Foundation"
    elif any(k in q.lower() for k in ['stack', 'cycle', 'hashmap', 'bst', 'k largest', 'bfs', 'dfs', 'trie', 'pointers', 'sliding', 'binary search', 'merge', 'quick', 'recursion', 'backtracking', 'dp', 'greedy', 'dijkstra', 'xor']):
        cat = "Data Structures & Algorithms"
    elif any(k in q.lower() for k in ['process', 'thread', 'deadlock', 'thrashing', '3nf', 'bcnf', 'where', 'having', 'dirty read', 'http', 'url shortener']):
        cat = "Systems & Databases"
    elif any(k in q.lower() for k in ['event loop', 'useeffect', 'put', 'patch', 'rebase', 'merge']):
        cat = "Web Development"
    elif any(k in q.lower() for k in ['gradient', 'bias', 'f1', 'relu', 'attention', 'rag', 'llm', 'drift']):
        cat = "AI & Machine Learning"
    else:
        cat = "General"
        
    parsed_cards.append({"q": q, "a": a, "s": strat, "c": cat})

# Generate JS Array
js_array = "const qa_data = [\n"
for c in parsed_cards:
    q_safe = c['q'].replace("'", "\\'")
    a_safe = c['a'].replace("'", "\\'")
    s_safe = c['s'].replace("'", "\\'")
    js_array += f"  {{ c: '{c['c']}', q: '{q_safe}', a: '{a_safe}', s: '{s_safe}' }},\n"
js_array += "];"


# Replace qa-grid and styles
new_css = """
        .qa-container { max-width: 960px; margin: 4rem auto 0; padding: 0 1.5rem 6rem; padding-top: 60px; }
        .qa-hero { margin-bottom: 3rem; text-align: center; }
        .qa-hero h1 { font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 12px; letter-spacing: -0.02em; }
        .qa-hero p { font-size: 1.1rem; color: var(--text-secondary); max-width: 650px; margin: 0 auto; line-height: 1.6; }
        
        /* Tracker Matching Styles */
        .acc-block { margin-bottom: 0.75rem; border: 0.5px solid var(--border); border-radius: 12px; overflow: hidden; background: var(--surface-1); }
        .acc-header { padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; cursor: pointer; user-select: none; background: var(--surface-2); }
        .acc-title { font-size: 14px; font-weight: 600; color: var(--text-primary); }
        .acc-content { display: none; padding: 0 1.25rem 1rem; border-top: 0.5px solid var(--border); }
        .acc-block.expanded .acc-content { display: block; }
        .acc-icon { font-size: 18px; color: var(--text-muted); transition: transform 0.2s; }
        .acc-block.expanded .acc-icon { transform: rotate(180deg); }
        
        .t-row { border-bottom: 0.5px solid var(--border); transition: background 0.15s; }
        .t-row:last-child { border-bottom: none; }
        .t-head { display: flex; align-items: center; gap: 10px; padding: 0.75rem 0; cursor: pointer; position: relative; }
        .t-num { font-size: 11px; color: var(--text-muted); min-width: 22px; font-weight: 600; }
        .t-name { font-size: 13px; color: var(--text-primary); flex: 1; }
        
        /* The expanded Q&A details */
        .q-details { display: none; padding: 0.5rem 0 1.25rem 32px; }
        .t-row.open .q-details { display: block; }
        .t-row.open .t-name { color: var(--brand); font-weight: 600; }
        
        .qa-a { font-size: 13.5px; color: var(--text-secondary); line-height: 1.55; margin-bottom: 12px; }
        .qa-premium-tip { background: rgba(255, 94, 0, 0.05); border: 1px solid rgba(255, 94, 0, 0.2); border-radius: 8px; padding: 1rem 1.25rem; display: flex; gap: 12px; align-items: flex-start; }
        .qa-premium-tip-icon { color: var(--brand); font-size: 1.2rem; margin-top: 2px; }
        .qa-premium-tip-text { font-size: 13px; color: var(--text-primary); line-height: 1.5; }
        .qa-premium-tip-text b { color: var(--brand); font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; display: block; margin-bottom: 4px; }
"""

new_html_js = """
        <div id="qaList"></div>
    </div>
    
    <script>
      """ + js_array + """
      
      function renderQA() {
          const list = document.getElementById('qaList');
          let html = '';
          let curBlock = '';
          let blockRows = '';
          let qNum = 1;
          
          const closeBlock = () => {
            if(curBlock !== '') {
               html += `
               <div class="acc-block expanded">
                 <div class="acc-header" onclick="this.parentElement.classList.toggle('expanded')">
                   <span class="acc-title">${curBlock}</span>
                   <i class="ti ti-chevron-down acc-icon"></i>
                 </div>
                 <div class="acc-content">
                   ${blockRows}
                 </div>
               </div>`;
            }
          };

          qa_data.forEach((t, i) => {
            if(t.c !== curBlock){
              closeBlock();
              curBlock = t.c;
              blockRows = '';
              qNum = 1;
            }
            
            blockRows += `
            <div class="t-row" onclick="this.classList.toggle('open')">
              <div class="t-head">
                <span class="t-num">${qNum}</span>
                <span class="t-name">Q: ${t.q}</span>
              </div>
              <div class="q-details">
                <div class="qa-a">${t.a}</div>
                <div class="qa-premium-tip">
                    <span class="qa-premium-tip-icon">💡</span>
                    <div class="qa-premium-tip-text">
                        <b>Premium Strategy</b>
                        ${t.s}
                    </div>
                </div>
              </div>
            </div>`;
            qNum++;
          });
          
          closeBlock();
          list.innerHTML = html;
      }
      
      renderQA();
      
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
"""

# Apply Regex substitutions
# 1. Replace the styles
content = re.sub(r'\.qa-container \{.*?\.qa-premium-tip-text b \{.*?\}', new_css, content, flags=re.DOTALL)
# 2. Add Tabler icons if missing
if 'tabler-icons' not in content:
    content = content.replace('</title>', '</title>\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">')

# 3. Replace the grid and scripts
content = re.sub(r'<div class="qa-grid">.*?<script>', new_html_js.replace('<script>', ''), content, flags=re.DOTALL)

with open(file_path, 'w') as f:
    f.write(content)

print("Interview QA rebuilt.")
