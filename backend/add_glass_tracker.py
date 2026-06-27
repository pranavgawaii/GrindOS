import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
TRACKER = os.path.join(FRONTEND, "tracker.html")

with open(TRACKER, 'r') as f:
    content = f.read()

# 1. Add Glass CSS
glass_css = """
/* Glass Mastery Tracker */
.mastery-glass { margin-top:2.5rem; background:var(--surface-1); padding:1.25rem; border-radius:12px; border:1px solid var(--border); box-shadow: 0 4px 15px rgba(0,0,0,0.1); position:relative; overflow:hidden; }
.mastery-glass::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: var(--brand); opacity: 0.5; }
.fp-track { height:6px; background:var(--surface-0); border-radius:3px; overflow:hidden; }
.fp-fill { height:100%; background:var(--text-1); border-radius:3px; width:0%; transition:width 0.4s ease-out; }
"""
if 'mastery-glass' not in content:
    content = content.replace('<style>', '<style>\n' + glass_css + '\n', 1)

# 2. Add Glass HTML at the end of pg-checkin
glass_html = """
  <div class="mastery-glass">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
      <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.06em;">Overall Grind Mastery</span>
      <span style="font-size:0.85rem; font-weight:700; color:var(--text-1);" id="fp-pct">0%</span>
    </div>
    <div class="fp-track"><div class="fp-fill" id="fp-fill"></div></div>
  </div>
"""
if 'mastery-glass' not in content.split('pg-checkin')[1]:
    # find where pg-checkin ends
    content = content.replace('  <div class="topic-list" id="topicList"></div>\n</div>', '  <div class="topic-list" id="topicList"></div>\n' + glass_html + '\n</div>')

# 3. Rewrite renderTopics to include block progress and update glass tracker
new_render_topics = """
function renderTopics(){
  const list=document.getElementById('topicList');
  let html='';
  let curBlock='';
  let overdueCount=0;
  let blockRows = '';
  
  let blockTotal = 0;
  let blockDone = 0;
  
  const closeBlock = () => {
    if(curBlock !== '') {
       let tickBadge = blockDone === blockTotal && blockTotal > 0 ? 
         `<div style="display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:4px;background:#3B6D11;color:white;"><i class="ti ti-check" style="font-size:12px"></i></div>` :
         `<span style="font-size:11px;color:var(--text-muted);font-weight:600;background:var(--surface-0);padding:2px 8px;border-radius:20px;border:1px solid var(--border);">${blockDone} / ${blockTotal}</span>`;
         
       html += `
       <div class="acc-block">
         <div class="acc-header" onclick="this.parentElement.classList.toggle('expanded')">
           <span class="acc-title">${curBlock}</span>
           <div style="display:flex;align-items:center;gap:10px;">
             ${tickBadge}
             <i class="ti ti-chevron-down acc-icon"></i>
           </div>
         </div>
         <div class="acc-content">
           <div class="topic-list">
             ${blockRows}
           </div>
         </div>
       </div>`;
    }
  };

  topics.forEach((t,i)=>{
    if(t.b!==curBlock){
      closeBlock();
      curBlock=t.b;
      blockRows = '';
      blockTotal = 0;
      blockDone = 0;
    }
    blockTotal++;
    const isChecked = checked.has(i);
    if(isChecked) blockDone++;
    
    const status=getDueStatus(t.due);
    if(status==='overdue'&&!isChecked) overdueCount++;
    const doneClass=isChecked?'checked':'';
    const tag=status==='overdue'&&!isChecked?`<span class="overdue-tag">overdue</span>`:status==='today'&&!isChecked?`<span class="due-tag">due today</span>`:'';
    
    blockRows += `<div class="t-row" id="tr${i}">
      <div class="t-head">
        <span class="t-num">${t.n}</span>
        <span class="t-name">${t.name}</span>
        ${tag}
        <span class="t-date">${t.due}</span>
        <div class="t-cb ${doneClass}" onclick="event.stopPropagation();tryCheck(${i})" id="cb${i}"><i class="ti ti-check" aria-hidden="true"></i></div>
      </div>
    </div>`;
  });
  
  closeBlock(); // close the very last block
  
  list.innerHTML=html;
  
  // Update stats
  document.getElementById('sOver').textContent=overdueCount;
  document.getElementById('sDone').textContent=checked.size;
  document.getElementById('sLeft').textContent=51-checked.size;
  
  // Update glass tracker
  const fpPct = document.getElementById('fp-pct');
  const fpFill = document.getElementById('fp-fill');
  if(fpPct && fpFill) {
      const pct = Math.round((checked.size/51)*100);
      fpPct.textContent = pct + '%';
      fpFill.style.width = pct + '%';
  }
}
"""

content = re.sub(r'function renderTopics\(\)\{.*?(?=function tryCheck)', new_render_topics, content, flags=re.DOTALL)

with open(TRACKER, 'w') as f:
    f.write(content)

print("Glass component and block progress badges added successfully.")
