import os
import re
from datetime import datetime, timedelta

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
START_DATE = datetime(2026, 6, 26)

# 1. Parse Notebook for topics
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()

guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

blocks_data = []
current_block = None

for line in lines:
    text = re.sub(r'<[^>]+>', '', line).strip()
    block_match = re.search(r'###\s*(BLOCK\s+(\d+)\s*[—\-]\s*[^\(]+)', text)
    if block_match:
        block_title = block_match.group(1).strip()
        clean_title = re.sub(r'BLOCK\s+\d+\s*[—\-]\s*', '', block_title)
        block_num = int(block_match.group(2))
        current_block = {"num": block_num, "title": clean_title, "items": [], "days": 0, "resources": "", "notes": "", "tips": ""}
        blocks_data.append(current_block)
        continue
        
    if current_block:
        topic_match = re.match(r'^(\d+)\.\s+(.*)', text)
        if topic_match:
            current_block["items"].append({
                "type": "topic",
                "id": topic_match.group(1),
                "text": topic_match.group(2)
            })
        else:
            subtopic_match = re.match(r'^-\s+(.*)', text)
            if subtopic_match:
                current_block["items"].append({
                    "type": "subtopic",
                    "id": f"{current_block['items'][-1]['id'] if current_block['items'] else '0'}_sub_{len(current_block['items'])}",
                    "text": subtopic_match.group(1)
                })

# 2. Parse Roadmap
roadmap_path = "/Users/8teen/Downloads/fresher_placement_roadmap.html"
with open(roadmap_path, "r") as f:
    rm_content = f.read()

rm_blocks = rm_content.split('<div class="block">')[1:]
for rm_block in rm_blocks:
    num_match = re.search(r'<div class="block-num">Block (\d+)', rm_block)
    if not num_match: continue
    b_num = int(num_match.group(1))
    
    target_block = next((b for b in blocks_data if b["num"] == b_num), None)
    if not target_block: continue
    
    dur_match = re.search(r'>(\d+)\s*days<', rm_block)
    if dur_match: target_block["days"] = int(dur_match.group(1))
    
    res_match = re.search(r'<div class="res-row">(.*?)</div>\s*<div class="', rm_block, flags=re.DOTALL)
    if not res_match: res_match = re.search(r'<div class="res-row">(.*?)</div>\s*</div>', rm_block, flags=re.DOTALL)
    if res_match: target_block["resources"] = res_match.group(1).strip()
    notes_match = re.search(r'<div class="note-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if notes_match: target_block["notes"] = notes_match.group(1).strip()
    tips_match = re.search(r'<div class="tip-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if tips_match: target_block["tips"] = tips_match.group(1).strip()

# 3. Calculate Live Dates
current_date = START_DATE
total_topics = sum(len(b["items"]) for b in blocks_data)

for block in blocks_data:
    block_start_date = current_date
    block["start_date"] = block_start_date
    block["end_date"] = block_start_date + timedelta(days=block["days"])
    
    num_items = len(block["items"])
    if num_items > 0:
        days_per_item = block["days"] / num_items
        for i, item in enumerate(block["items"]):
            item_date = block_start_date + timedelta(days=(i+1)*days_per_item)
            item["due_date"] = item_date
            
    current_date = block["end_date"]


# 4. Generate Tracker HTML
css = """
<style>
/* Metrics Matrix */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 2.5rem; }
.metric-box { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); position: relative; overflow: hidden;}
.metric-box::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: var(--brand); opacity: 0.5; }
.metric-val { font-size: 1.8rem; font-weight: 800; color: var(--text-1); line-height: 1; margin-bottom: 4px; }
.metric-lbl { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); font-weight: 600;}
.overdue-val { color: #ff4757 !important; }
.overdue-box::before { background: #ff4757; opacity: 1; }

.checklist-master-container { max-width: 900px; margin: 0 auto; padding: 0 1rem; padding-bottom: 120px; text-align: left; }
.tracker-hero { margin-bottom: 2rem; padding: 1rem 0; text-align: center; }
.tracker-hero h1 { font-size: 2rem; font-weight: 800; color: var(--text-1); margin-bottom: 0.5rem; }

/* Accordions */
.acc-card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 1.5rem; overflow: hidden; transition: border-color 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.acc-header { padding: 1.25rem 1.5rem; background: var(--surface-2); display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; }
.acc-header-left { display: flex; flex-direction: column; gap: 4px; text-align: left; }
.acc-title { font-size: 1.15rem; font-weight: 700; color: var(--text-1); letter-spacing: 0.02em; }
.acc-date-pill { display: inline-flex; align-items: center; gap: 6px; font-size: 0.8rem; color: var(--brand); font-weight: 600; padding: 4px 10px; background: rgba(255, 94, 0, 0.1); border-radius: 20px; border: 1px solid rgba(255, 94, 0, 0.2); width: fit-content; margin-top: 4px;}
.acc-chevron { transition: transform 0.3s; color: var(--text-3); }
.acc-card.open .acc-chevron { transform: rotate(180deg); }
.acc-body { display: none; padding: 1.5rem; border-top: 1px solid var(--border); }
.acc-card.open .acc-body { display: block; }

/* Checklist - Left Aligned explicitly */
.task-list { display: flex; flex-direction: column; gap: 4px; margin-bottom: 2rem; text-align: left; }
.task-item { display: flex; align-items: flex-start; justify-content: flex-start; gap: 14px; padding: 10px 14px; border-radius: 8px; cursor: pointer; transition: background 0.2s; text-align: left; width: 100%; box-sizing: border-box;}
.task-item:hover { background: var(--surface-0); }
.task-item.subtopic { margin-left: 2.5rem; width: calc(100% - 2.5rem); position: relative; }
.task-item.subtopic::before { content: ''; position: absolute; left: -14px; top: -10px; bottom: 50%; width: 2px; background: var(--border); border-bottom-left-radius: 4px;}
.task-item.subtopic::after { content: ''; position: absolute; left: -14px; top: 50%; width: 14px; height: 2px; background: var(--border); }

.task-checkbox { display: none; }
.task-custom-check { width: 20px; height: 20px; border-radius: 5px; border: 2px solid var(--text-4); display: flex; align-items: center; justify-content: center; margin-top: 2px; flex-shrink: 0; background: transparent; transition: all 0.2s;}
.task-checkbox:checked + .task-custom-check { background: var(--text-1); border-color: var(--text-1); }
.task-checkbox:checked + .task-custom-check::after { content: '\\2713'; color: var(--bg); font-size: 14px; font-weight: bold; }

.task-content { flex: 1; display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; text-align: left;}
.task-title-wrap { display: flex; align-items: flex-start; text-align: left;}
.task-title { font-size: 0.95rem; color: var(--text-1); line-height: 1.5; text-align: left; }
.task-checkbox:checked ~ .task-content .task-title { color: var(--text-4); text-decoration: line-through; }
.task-num { font-weight: 700; margin-right: 6px; color: var(--brand); }

/* Overdue Badge */
.task-due { font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 12px; white-space: nowrap; margin-top: 2px; display: inline-flex; align-items: center;}
.due-normal { color: var(--text-muted); background: var(--surface-0); border: 1px solid var(--border); }
.due-overdue { color: #ff4757; background: rgba(255, 71, 87, 0.1); border: 1px solid rgba(255, 71, 87, 0.2); }
.task-checkbox:checked ~ .task-content .task-due { opacity: 0.5; text-decoration: line-through;}

/* Meta */
.acc-meta { display: flex; flex-direction: column; gap: 1.25rem; padding-top: 1.5rem; border-top: 1px solid var(--border-light); text-align: left;}
.meta-section h4 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.75rem; text-align: left;}
.info-box { padding: 1rem; border-radius: 8px; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0.5rem; text-align: left;}
.box-note { background: rgba(245, 166, 35, 0.1); border: 1px solid rgba(245, 166, 35, 0.2); color: var(--text-1); }
.box-note b { color: #f5a623; }
.box-tip { background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); color: var(--text-1); }
.box-tip b { color: #2ed573; }
.res-links { display: flex; flex-direction: column; gap: 8px; }
.res-links a { display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: var(--surface-0); border: 1px solid var(--border); border-radius: 8px; color: var(--text-1); text-decoration: none; font-size: 0.9rem; transition: border-color 0.2s; text-align: left;}
.res-links a:hover { border-color: var(--text-3); }

/* Floating Progress - No Button */
.floating-progress { position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); background: var(--surface-2); border: 1px solid var(--border-strong); border-radius: 100px; padding: 14px 28px; display: flex; align-items: center; width: 90%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); z-index: 1000; backdrop-filter: blur(10px); }
.fp-stats { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.fp-text { font-size: 0.85rem; font-weight: 600; color: var(--text-2); display: flex; justify-content: space-between;}
.fp-bar-bg { width: 100%; height: 8px; background: var(--surface-0); border-radius: 4px; overflow: hidden; }
.fp-bar-fill { height: 100%; background: var(--text-1); border-radius: 4px; width: 0%; transition: width 0.3s; }
</style>
"""

blocks_html = ""
for block in blocks_data:
    if not block["items"]: continue
    
    items_html = ""
    for item in block["items"]:
        is_sub = "subtopic" if item["type"] == "subtopic" else "topic"
        prefix = f"<span class='task-num'>{item['id']}.</span>" if is_sub == "topic" else ""
        date_str = item["due_date"].strftime("%b %d, %Y")
        due_iso = item["due_date"].strftime("%Y-%m-%d")
        
        items_html += f"""
        <label class="task-item {is_sub}">
            <input type="checkbox" class="task-checkbox" id="topic-{item['id']}" data-due="{due_iso}">
            <div class="task-custom-check"></div>
            <div class="task-content">
                <div class="task-title-wrap">
                    <span class="task-title">{prefix}{item['text']}</span>
                </div>
                <span class="task-due due-normal" id="badge-{item['id']}">{date_str}</span>
            </div>
        </label>
        """
        
    meta_html = ""
    if block["resources"] or block["notes"] or block["tips"]:
        res_html = f"<div class='meta-section'><h4>Resources</h4><div class='res-links'>{block['resources']}</div></div>" if block['resources'] else ""
        notes_html = f"<div class='meta-section'><h4>Notes Strategy</h4><div class='info-box box-note'>{block['notes']}</div></div>" if block['notes'] else ""
        tips_html = f"<div class='meta-section'><h4>Tips & Tricks</h4><div class='info-box box-tip'>{block['tips']}</div></div>" if block['tips'] else ""
        meta_html = f"<div class='acc-meta'>{res_html}{notes_html}{tips_html}</div>"
        
    start_str = block["start_date"].strftime("%b %d, %Y")
    end_str = block["end_date"].strftime("%b %d, %Y")
        
    blocks_html += f"""
    <div class="acc-card" onclick="toggleAcc(this)">
        <div class="acc-header">
            <div class="acc-header-left">
                <div class="acc-title">{block['title']}</div>
                <div class="acc-date-pill">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    Target: {start_str} - {end_str}
                </div>
            </div>
            <div class="acc-chevron">
                <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </div>
        </div>
        <div class="acc-body" onclick="event.stopPropagation()">
            <div class="task-list">
                {items_html}
            </div>
            {meta_html}
        </div>
    </div>
    """

new_tracker_html = f"""
        {css}
        <div class="checklist-master-container" id="checklist-master">
            <div class="tracker-hero">
                <h1>Roadmap Tracker</h1>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-box">
                    <span class="metric-val" id="m-total">{total_topics}</span>
                    <span class="metric-lbl">Total Tasks</span>
                </div>
                <div class="metric-box">
                    <span class="metric-val" id="m-completed">0</span>
                    <span class="metric-lbl">Completed</span>
                </div>
                <div class="metric-box">
                    <span class="metric-val" id="m-remaining">{total_topics}</span>
                    <span class="metric-lbl">Remaining</span>
                </div>
                <div class="metric-box overdue-box">
                    <span class="metric-val overdue-val" id="m-overdue">0</span>
                    <span class="metric-lbl">Overdue</span>
                </div>
            </div>
            
            <div class="blocks-container">
                {blocks_html}
            </div>
        </div>
        
        <div class="floating-progress">
            <div class="fp-stats">
                <div class="fp-text">
                    <span>Overall Mastery</span> <span id="fp-count">0%</span>
                </div>
                <div class="fp-bar-bg">
                    <div class="fp-bar-fill" id="fp-bar"></div>
                </div>
            </div>
        </div>
        
        <script>
            function toggleAcc(el) {{
                const isOpen = el.classList.contains('open');
                if (!isOpen) el.classList.add('open');
                else el.classList.remove('open');
            }}
            function updateNewProgress() {{
                const checkboxes = document.querySelectorAll('.task-checkbox');
                const total = checkboxes.length;
                let checked = 0;
                let overdueCount = 0;
                
                const today = new Date();
                today.setHours(0,0,0,0);
                
                checkboxes.forEach(cb => {{
                    const isChecked = cb.checked;
                    if (isChecked) checked++;
                    
                    // Overdue logic
                    const dueDateStr = cb.getAttribute('data-due');
                    const badge = document.getElementById('badge-' + cb.id.split('-')[1]);
                    
                    if (dueDateStr) {{
                        const dueDate = new Date(dueDateStr);
                        if (!isChecked && dueDate < today) {{
                            overdueCount++;
                            badge.classList.remove('due-normal');
                            badge.classList.add('due-overdue');
                            badge.innerHTML = 'Overdue (' + dueDateStr + ')';
                        }} else {{
                            badge.classList.remove('due-overdue');
                            badge.classList.add('due-normal');
                            badge.innerHTML = dueDateStr;
                        }}
                    }}
                }});
                
                // Update Matrix
                document.getElementById('m-completed').textContent = checked;
                document.getElementById('m-remaining').textContent = total - checked;
                document.getElementById('m-overdue').textContent = overdueCount;
                
                // Update Progress Pill
                const pct = total === 0 ? 0 : Math.round((checked / total) * 100);
                document.getElementById('fp-count').innerHTML = pct + "%";
                document.getElementById('fp-bar').style.width = pct + "%";
            }}
            
            document.querySelectorAll('.task-checkbox').forEach(cb => {{
                cb.addEventListener('change', updateNewProgress);
                const saved = localStorage.getItem('grindos-task-' + cb.id);
                if (saved === 'true') cb.checked = true;
                cb.addEventListener('change', (e) => {{
                    localStorage.setItem('grindos-task-' + cb.id, e.target.checked);
                }});
            }});
            
            if (document.readyState === 'complete') updateNewProgress();
            else window.addEventListener('DOMContentLoaded', updateNewProgress);
        </script>
"""

# Redesign Notebook to Notion-style Sidebar Split Pane
notebook_css = """
<style>
/* Notion-style Notebook Redesign */
.nb-master-container {
    max-width: 1200px;
    margin: 4rem auto;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface-1);
    display: flex;
    overflow: hidden;
    height: 800px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.15);
}

.nb-sidebar {
    width: 280px;
    background: var(--surface-2);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
}
.nb-sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-light);
}
.nb-sidebar-header h2 { font-size: 1.2rem; font-weight: 700; margin: 0; color: var(--text-1); }
.nb-sidebar-header p { font-size: 0.8rem; color: var(--text-3); margin-top: 4px; }

.nb-tabs-vertical {
    padding: 1rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 4px;
    overflow-y: auto;
}
.nb-tab {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-2);
    transition: all 0.2s;
    text-align: left;
}
.nb-tab:hover { background: var(--surface-1); color: var(--text-1); }
.nb-tab.active { background: rgba(255, 94, 0, 0.1); color: var(--brand); font-weight: 600; }
.nb-tab svg { color: inherit; opacity: 0.7; }

/* The Right Pane */
.nb-content-pane {
    flex: 1;
    overflow-y: auto;
    background: var(--bg);
    position: relative;
}

.nb-page {
    display: none;
    padding: 4rem;
    max-width: 800px;
    margin: 0 auto;
}
.nb-page.active {
    display: block;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

.page-top {
    margin-bottom: 3rem;
}
.page-subject { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--brand); font-weight: 700; margin-bottom: 8px; }
.page-title { font-size: 2.4rem; font-weight: 800; color: var(--text-1); letter-spacing: -0.03em; line-height: 1.2;}
.page-date { font-size: 0.9rem; color: var(--text-3); margin-top: 1rem; }

/* Markdown Typography */
.ruled { padding: 0 !important; background: transparent !important; }
.line { margin-bottom: 0.75rem !important; border-bottom: none !important;}
.line-num { display: none !important; }
.line-content { font-family: 'Inter', sans-serif !important; font-size: 1.05rem !important; line-height: 1.7 !important; color: var(--text-2) !important; display: block;}

.hl-purple, .hl-blue, .hl-coral, .hl-teal { 
    display: block;
    font-size: 1.3rem; 
    font-weight: 700; 
    color: var(--text-1); 
    margin-top: 2.5rem; 
    margin-bottom: 1rem; 
    border-bottom: 1px solid var(--border); 
    padding-bottom: 0.5rem;
}
.arrow { color: var(--brand); font-weight: bold; margin-right: 8px; }
.indent { padding-left: 1.5rem; position: relative; }
.indent::before { content: '•'; position: absolute; left: 0.5rem; color: var(--text-4); }

.sticky {
    margin-top: 3rem;
    padding: 1.5rem 2rem;
    background: var(--surface-1);
    border-left: 4px solid var(--brand);
    border-radius: 0 8px 8px 0;
}
.sticky-title { font-size: 1.1rem; font-weight: 700; color: var(--brand); margin-bottom: 0.5rem; }
.warn-box { margin-top: 2rem; padding: 1.5rem; background: rgba(255, 60, 60, 0.1); border: 1px solid rgba(255, 60, 60, 0.2); border-radius: 8px; color: var(--text-1); font-weight: 500;}

/* Hide old header */
.dashboard-header-row:has(h2:contains("Interview Notes Notebook")) { display: none; }
</style>
"""

def redesign_notebook(html):
    # Hide the old header and wrapper container
    html = re.sub(r'<div class="dashboard-header-row"[^>]*>\s*<div class="dashboard-title-area">\s*<h2>Interview Notes Notebook</h2>.*?</div>\s*</div>', '', html, flags=re.DOTALL)
    
    # We will replace the <div class="nb-wrap"> and the <div class="nb-tabs"> entirely
    # The structure will be:
    # <div class="nb-master-container">
    #   <div class="nb-sidebar"> ... tabs ... </div>
    #   <div class="nb-content-pane"> ... pages ... </div>
    # </div>
    
    sidebar = """
    <div class="nb-master-container">
        <div class="nb-sidebar">
            <div class="nb-sidebar-header">
                <h2>Interview Notes</h2>
                <p>Digital Markdown Workspace</p>
            </div>
            <div class="nb-tabs-vertical">
                <div class="nb-tab active" onclick="switchTab('os')">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    OS — Deadlock
                </div>
                <div class="nb-tab" onclick="switchTab('dbms')">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    DBMS — SQL
                </div>
                <div class="nb-tab" onclick="switchTab('tips')">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    Tips + Tricks
                </div>
                <div class="nb-tab" onclick="switchTab('playbook')">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    Fresher Playbook
                </div>
            </div>
        </div>
        <div class="nb-content-pane">
    """
    
    # Locate <div class="nb-wrap"> and replace it and the old tabs
    pattern = r'<div class="glass-card stat-card"[^>]*>\s*<div class="nb-wrap">\s*<div class="nb-tabs">.*?</div>'
    html = re.sub(pattern, notebook_css + sidebar, html, flags=re.DOTALL)
    
    # Make sure we close the two new divs at the very end. The old one closed `nb-wrap` and `stat-card`.
    # Let's just find the end of the playbook tab and replace the closing divs.
    end_pattern = r'</div>\s*</div>\s*</div>\s*(?=<script>)'
    
    # Wait, instead of regex for the closing, let's just do a simple replacement
    html = html.replace('</div>\n    </div>\n  </div>\n</div>\n\n<script>', '</div>\n</div>\n<script>')
    
    return html

def apply_updates(html):
    start_tag = '<div class="checklist-master-container"'
    start_idx = html.find(start_tag)
    if start_idx != -1:
        end_idx = html.find('</script>', start_idx) + len('</script>')
        html = html[:start_idx] + new_tracker_html + html[end_idx:]
        
    html = redesign_notebook(html)
    return html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            html = f.read()
        new_html = apply_updates(html)
        with open(path, "w") as f:
            f.write(new_html)

print("V4 Updates Complete: Matrix, Left-align, Overdue Logic, Notion-Style Notebook.")
