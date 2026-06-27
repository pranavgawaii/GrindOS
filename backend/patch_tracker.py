import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
TRACKER = os.path.join(FRONTEND, "tracker.html")
CHECKIN_SYS = os.path.join(ROOT, "grindos_checkin_system.html")

with open(TRACKER, 'r') as f:
    content = f.read()

# 1. Inject the missing Check In system CSS
with open(CHECKIN_SYS, 'r') as f:
    sys_content = f.read()
    
sys_style_match = re.search(r'<style>(.*?)</style>', sys_content, re.DOTALL)
if sys_style_match:
    sys_style = sys_style_match.group(1).strip()
    # Add some accordion CSS
    sys_style += """
/* Accordion Additions */
.acc-block { margin-bottom: 0.75rem; border: 0.5px solid var(--border); border-radius: 12px; overflow: hidden; background: var(--surface-1); }
.acc-header { padding: 1rem 1.25rem; display: flex; align-items: center; justify-content: space-between; cursor: pointer; user-select: none; background: var(--surface-2); }
.acc-title { font-size: 14px; font-weight: 600; color: var(--text-primary); }
.acc-content { display: none; padding: 0 1.25rem 1rem; border-top: 0.5px solid var(--border); }
.acc-block.expanded .acc-content { display: block; }
.acc-icon { font-size: 18px; color: var(--text-muted); transition: transform 0.2s; }
.acc-block.expanded .acc-icon { transform: rotate(180deg); }
"""
    # Insert it before the Notebook style
    content = content.replace('<style>', '<style>\n' + sys_style + '\n', 1)

# 2. Rewrite renderTopics()
new_render_topics = """
function renderTopics(){
  const list=document.getElementById('topicList');
  let html='';
  let curBlock='';
  let overdueCount=0;
  let blockRows = '';
  
  // Close the last block helper
  const closeBlock = () => {
    if(curBlock !== '') {
       html += `
       <div class="acc-block">
         <div class="acc-header" onclick="this.parentElement.classList.toggle('expanded')">
           <span class="acc-title">${curBlock}</span>
           <i class="ti ti-chevron-down acc-icon"></i>
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
    }
    const status=getDueStatus(t.due);
    if(status==='overdue'&&!checked.has(i)) overdueCount++;
    const doneClass=checked.has(i)?'checked':'';
    const tag=status==='overdue'&&!checked.has(i)?`<span class="overdue-tag">overdue</span>`:status==='today'&&!checked.has(i)?`<span class="due-tag">due today</span>`:'';
    
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
  document.getElementById('sOver').textContent=overdueCount;
  document.getElementById('sDone').textContent=checked.size;
  document.getElementById('sLeft').textContent=51-checked.size;
}
"""

# Regex to replace the old renderTopics() block
content = re.sub(r'function renderTopics\(\)\{.*?(?=function expandRow|function tryCheck)', new_render_topics, content, flags=re.DOTALL)

# Also remove expandRow() entirely since it's no longer used
content = re.sub(r'function expandRow\(i\)\{.*?\}', '', content, flags=re.DOTALL)

with open(TRACKER, 'w') as f:
    f.write(content)

print("Tracker patched successfully.")
