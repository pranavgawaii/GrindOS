import re
import json

file_path = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/interview_qa.html"
with open(file_path, 'r') as f:
    content = f.read()

# Split the content before the hero
top_half = content.split('<div class="qa-container">')[0]

# Add more fresher questions
extra_qs = [
  "{ c: 'General', q: 'What is OOP?', a: 'Object-Oriented Programming is a paradigm based on objects, containing data (attributes) and code (methods). The four pillars are Encapsulation, Abstraction, Inheritance, and Polymorphism.', s: 'List all four pillars immediately, then define them concisely if asked.' }",
  "{ c: 'General', q: 'Compiler vs Interpreter?', a: 'A compiler translates the entire source code into machine code before execution. An interpreter translates code line-by-line during execution.', s: 'Mention that Java uses both (compiled to bytecode, then interpreted/JIT compiled by JVM).' }",
  "{ c: 'Systems & Databases', q: 'What is an API?', a: 'Application Programming Interface. It allows different software applications to communicate with each other using a defined set of rules.', s: 'Use the restaurant analogy: The menu is the UI, the kitchen is the backend, and the waiter is the API taking your order to the kitchen.' }",
  "{ c: 'Systems & Databases', q: 'What is SQL vs NoSQL?', a: 'SQL is relational, structured, and uses tables with strict schemas. NoSQL is non-relational, document-based (like JSON), and flexible.', s: 'Mention scaling: SQL scales vertically (add more CPU/RAM), NoSQL scales horizontally (add more servers).' }",
  "{ c: 'Data Structures & Algorithms', q: 'What is a pointer?', a: 'A variable that stores the memory address of another variable rather than its direct value.', s: 'Mention that Python hides pointers from the user for safety, but uses them under the hood (e.g., references).' }",
]

# Extract the existing qa_data
qa_data_match = re.search(r'const qa_data = \[\s*(.*?)\s*\];', content, re.DOTALL)
if qa_data_match:
    qa_data_str = qa_data_match.group(1)
else:
    qa_data_str = ""

all_qa = qa_data_str + ",\n  " + ",\n  ".join(extra_qs)

# Clean up trailing commas in the array body
all_qa = re.sub(r',\s*,', ',', all_qa)

new_content = top_half + """<div class="qa-container">
        <div class="qa-hero">
            <h1>Ultimate Interview Q&A</h1>
            <p>Don't just answer the question — dominate it. These are high-yield questions across all CS domains, formulated with premium interview strategies that signal deep expertise.</p>
        </div>
        
        <div class="search-container" style="margin-bottom: 30px; position: relative;">
            <i class="ti ti-search" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 20px;"></i>
            <input type="text" id="qaSearch" placeholder="Search topics or questions (e.g., 'Python', 'OOP', 'hashmap')..." onkeyup="filterQA()" style="width: 100%; padding: 16px 16px 16px 48px; border-radius: 12px; border: 1px solid var(--border); background: var(--surface-1); color: var(--text-primary); font-size: 16px; outline: none; transition: border-color 0.2s;">
        </div>
        
        <div id="qaList"></div>
    </div>
    
    <script>
      const qa_data = [
        """ + all_qa + """
      ];
      
      function renderQA(dataToRender) {
          const list = document.getElementById('qaList');
          let html = '';
          let curBlock = '';
          let blockRows = '';
          let qNum = 1;
          
          if (dataToRender.length === 0) {
              list.innerHTML = `<div style="text-align:center; color: var(--text-muted); padding: 40px;">No questions found matching your search.</div>`;
              return;
          }
          
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

          dataToRender.forEach((t, i) => {
            if(t.c !== curBlock){
              closeBlock();
              curBlock = t.c;
              blockRows = '';
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
      
      function filterQA() {
          const query = document.getElementById('qaSearch').value.toLowerCase();
          if (!query) {
              renderQA(qa_data);
              return;
          }
          
          const filtered = qa_data.filter(t => 
              t.c.toLowerCase().includes(query) || 
              t.q.toLowerCase().includes(query) || 
              t.a.toLowerCase().includes(query)
          );
          renderQA(filtered);
      }
      
      // Initial render
      renderQA(qa_data);
      
      (function() {
        const toggle = document.getElementById('theme-toggle');
        if(toggle) {
          toggle.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('GrindOS-theme', isDark ? 'dark' : '');
          });
        }
        
        // Add focus style to search
        const searchInput = document.getElementById('qaSearch');
        if (searchInput) {
            searchInput.addEventListener('focus', () => searchInput.style.borderColor = 'var(--brand)');
            searchInput.addEventListener('blur', () => searchInput.style.borderColor = 'var(--border)');
        }
      })();
    </script>
<script src="assets/script.js?v=21"></script>
</body>
</html>"""

with open(file_path, 'w') as f:
    f.write(new_content)

print("QA Page fixed and Search Bar added.")
