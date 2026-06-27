import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# 1. Parse Notebook for topics
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()

guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

blocks_data = []
current_block = None
total_topics = 0

for line in lines:
    text = re.sub(r'<[^>]+>', '', line).strip()
    block_match = re.search(r'###\s*(BLOCK\s+(\d+)\s*[—\-]\s*[^\(]+)', text)
    if block_match:
        block_title = block_match.group(1).strip()
        block_num = int(block_match.group(2))
        current_block = {"num": block_num, "title": block_title, "items": [], "days": "", "resources": "", "notes": "", "tips": ""}
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
            total_topics += 1
        else:
            subtopic_match = re.match(r'^-\s+(.*)', text)
            if subtopic_match:
                current_block["items"].append({
                    "type": "subtopic",
                    "id": f"{current_block['items'][-1]['id'] if current_block['items'] else '0'}_sub_{len(current_block['items'])}",
                    "text": subtopic_match.group(1)
                })
                total_topics += 1

# 2. Parse Roadmap for tips/tricks/resources/dates
roadmap_path = "/Users/8teen/Downloads/fresher_placement_roadmap.html"
with open(roadmap_path, "r") as f:
    rm_content = f.read()

# Extract blocks from roadmap
rm_blocks = rm_content.split('<div class="block">')[1:]
for rm_block in rm_blocks:
    num_match = re.search(r'<div class="block-num">Block (\d+)', rm_block)
    if not num_match: continue
    b_num = int(num_match.group(1))
    
    # Find matching block in blocks_data
    target_block = next((b for b in blocks_data if b["num"] == b_num), None)
    if not target_block: continue
    
    # Extract days
    days_match = re.search(r'· (Days [^<]+)</div>', rm_block)
    if days_match: target_block["days"] = days_match.group(1)
    
    # Extract resources HTML
    res_match = re.search(r'<div class="res-row">(.*?)</div>\s*<div class="', rm_block, flags=re.DOTALL)
    if not res_match:
        # fallback
        res_match = re.search(r'<div class="res-row">(.*?)</div>\s*</div>', rm_block, flags=re.DOTALL)
    if res_match: target_block["resources"] = res_match.group(1).strip()
    
    # Extract notes HTML
    notes_match = re.search(r'<div class="note-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if notes_match: target_block["notes"] = notes_match.group(1).strip()
    
    # Extract tips HTML
    tips_match = re.search(r'<div class="tip-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if tips_match: target_block["tips"] = tips_match.group(1).strip()


# 3. Build New UI
css = """
<style>
/* Ultra Premium Accordion Checklist */
.checklist-master-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 1rem;
    padding-bottom: 120px;
}
.tracker-hero {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem 0;
}
.tracker-hero h1 {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-1);
    margin-bottom: 0.5rem;
}
.tracker-hero p {
    font-size: 1.1rem;
    color: var(--text-3);
    max-width: 600px;
    margin: 0 auto;
}

/* Accordion Card */
.acc-card {
    background: var(--surface-1);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    overflow: hidden;
    transition: border-color 0.2s;
}
.acc-card:hover {
    border-color: var(--border-strong);
}
.acc-header {
    padding: 1.25rem 1.5rem;
    background: var(--surface-2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    user-select: none;
}
.acc-header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}
.acc-num {
    width: 36px; height: 36px;
    border-radius: 8px;
    background: var(--surface-0);
    border: 1px solid var(--border-strong);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: var(--text-1);
}
.acc-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-1);
}
.acc-days {
    font-size: 0.85rem;
    color: var(--text-3);
    margin-top: 4px;
}
.acc-chevron {
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: var(--text-3);
}
.acc-card.open .acc-chevron {
    transform: rotate(180deg);
}

.acc-body {
    display: none; /* hidden by default */
    padding: 1.5rem;
    border-top: 1px solid var(--border);
}
.acc-card.open .acc-body {
    display: block;
}

/* Checklist items */
.task-list { display: flex; flex-direction: column; gap: 4px; margin-bottom: 2rem; }
.task-item {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 10px 14px; border-radius: 8px;
    cursor: pointer; transition: background 0.2s;
}
.task-item:hover { background: var(--surface-0); }
.task-item.subtopic { margin-left: 2rem; }
.task-checkbox { display: none; }
.task-custom-check {
    width: 20px; height: 20px; border-radius: 5px;
    border: 2px solid var(--text-4);
    display: flex; align-items: center; justify-content: center;
    margin-top: 2px; flex-shrink: 0;
}
.task-checkbox:checked + .task-custom-check {
    background: var(--text-1); border-color: var(--text-1);
}
.task-checkbox:checked + .task-custom-check::after {
    content: '\\2713'; color: var(--bg); font-size: 14px; font-weight: bold;
}
.task-title { font-size: 0.95rem; color: var(--text-1); flex: 1; line-height: 1.5; }
.task-checkbox:checked ~ .task-title { color: var(--text-4); text-decoration: line-through; }
.task-num { font-weight: 700; margin-right: 6px; color: var(--text-2); }

/* Tips & Resources */
.acc-meta {
    display: flex; flex-direction: column; gap: 1.25rem;
    padding-top: 1.5rem; border-top: 1px solid var(--border-light);
}
.meta-section h4 {
    font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;
    color: var(--text-muted); margin-bottom: 0.75rem;
}
.info-box {
    padding: 1rem; border-radius: 8px; font-size: 0.9rem; line-height: 1.6;
    margin-bottom: 0.5rem;
}
.box-note { background: rgba(245, 166, 35, 0.1); border: 1px solid rgba(245, 166, 35, 0.2); color: var(--text-1); }
.box-note b { color: #f5a623; }
.box-tip { background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); color: var(--text-1); }
.box-tip b { color: #2ed573; }
.res-links { display: flex; flex-direction: column; gap: 8px; }
.res-links a {
    display: flex; align-items: center; gap: 8px;
    padding: 10px 14px; background: var(--surface-0); border: 1px solid var(--border);
    border-radius: 8px; color: var(--text-1); text-decoration: none; font-size: 0.9rem;
    transition: border-color 0.2s;
}
.res-links a:hover { border-color: var(--text-3); }

/* Clean Progress Bar */
.floating-progress {
    position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
    background: var(--surface-2); border: 1px solid var(--border-strong);
    border-radius: 100px; padding: 12px 24px; display: flex; align-items: center; gap: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3); z-index: 1000; width: 90%; max-width: 600px;
}
.fp-stats { flex: 1; }
.fp-text { font-size: 0.85rem; font-weight: 600; color: var(--text-2); margin-bottom: 6px; display: flex; justify-content: space-between;}
.fp-bar-bg { width: 100%; height: 6px; background: var(--surface-0); border-radius: 3px; overflow: hidden; }
.fp-bar-fill { height: 100%; background: var(--text-1); border-radius: 3px; width: 0%; transition: width 0.3s; }
.fp-save-btn {
    background: var(--text-1); color: var(--bg); border: none; padding: 10px 20px;
    border-radius: 100px; font-weight: 600; cursor: pointer;
}
</style>
"""

blocks_html = ""
for block in blocks_data:
    if not block["items"]: continue
    
    # Checklist
    items_html = ""
    for item in block["items"]:
        is_sub = "subtopic" if item["type"] == "subtopic" else "topic"
        prefix = f"<span class='task-num'>{item['id']}.</span>" if is_sub == "topic" else ""
        items_html += f"""
        <label class="task-item {is_sub}">
            <input type="checkbox" class="task-checkbox" id="topic-{item['id']}">
            <div class="task-custom-check"></div>
            <div class="task-title">{prefix}{item['text']}</div>
        </label>
        """
        
    # Meta (Tips/Notes/Resources)
    meta_html = ""
    if block["resources"] or block["notes"] or block["tips"]:
        res_html = f"<div class='meta-section'><h4>Resources</h4><div class='res-links'>{block['resources']}</div></div>" if block['resources'] else ""
        notes_html = f"<div class='meta-section'><h4>Notes Strategy</h4><div class='info-box box-note'>{block['notes']}</div></div>" if block['notes'] else ""
        tips_html = f"<div class='meta-section'><h4>Tips & Tricks</h4><div class='info-box box-tip'>{block['tips']}</div></div>" if block['tips'] else ""
        
        meta_html = f"""
        <div class="acc-meta">
            {res_html}
            {notes_html}
            {tips_html}
        </div>
        """
        
    blocks_html += f"""
    <div class="acc-card" onclick="toggleAcc(this)">
        <div class="acc-header">
            <div class="acc-header-left">
                <div class="acc-num">{block['num']}</div>
                <div>
                    <div class="acc-title">{block['title']}</div>
                    <div class="acc-days">{block['days']}</div>
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

new_html_block = f"""
        {css}
        <div class="checklist-master-container" id="checklist-master">
            <div class="tracker-hero">
                <h1>Roadmap Tracker</h1>
                <p>Master every topic step-by-step. Track your progress, follow the timeline, and use the provided resources.</p>
            </div>
            
            <div class="blocks-container">
                {blocks_html}
            </div>
        </div>
        
        <div class="floating-progress">
            <div class="fp-stats">
                <div class="fp-text">
                    <span>Progress</span> <span id="fp-count">0 / {total_topics}</span>
                </div>
                <div class="fp-bar-bg">
                    <div class="fp-bar-fill" id="fp-bar"></div>
                </div>
            </div>
            <button class="fp-save-btn">Save Progress</button>
        </div>
        
        <script>
            function toggleAcc(el) {{
                // Close others (optional, but requested just clicking opens it, we can toggle it)
                const isOpen = el.classList.contains('open');
                // document.querySelectorAll('.acc-card').forEach(c => c.classList.remove('open')); // Un-comment if only 1 open at a time
                if (!isOpen) el.classList.add('open');
                else el.classList.remove('open');
            }}
            
            function updateNewProgress() {{
                const checkboxes = document.querySelectorAll('.task-checkbox');
                const checked = document.querySelectorAll('.task-checkbox:checked').length;
                const total = checkboxes.length;
                
                document.getElementById('fp-count').innerHTML = checked + " / " + total;
                const pct = total === 0 ? 0 : (checked / total) * 100;
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

def apply_redesign(html):
    # 1. Strip the old Daily Check-In Header if it exists
    # The header looks like:
    # <div class="dashboard-header-row">
    #   <div class="dashboard-title-area">
    #     <h2>Daily Check-In</h2>
    # ...
    # </div>
    # </div>
    
    # We will search for the entire `dashboard-header-row` that contains Daily Check-In and remove it.
    import re
    html = re.sub(r'<div class="dashboard-header-row">.*?<h2>Daily Check-In</h2>.*?</div>\s*</div>', '', html, flags=re.DOTALL)
    
    # 2. Find the previous Master Checklist block and replace it
    start_tag = '<div class="checklist-master-container"'
    start_idx = html.find(start_tag)
    
    if start_idx != -1:
        # Find end of script
        end_idx = html.find('</script>', start_idx) + len('</script>')
        html = html[:start_idx] + new_html_block + html[end_idx:]
    
    return html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            html = f.read()
        new_html = apply_redesign(html)
        with open(path, "w") as f:
            f.write(new_html)

print("Redesign V3 deployed: Accoridons, Tips, No Gradients, Old Header Removed.")
