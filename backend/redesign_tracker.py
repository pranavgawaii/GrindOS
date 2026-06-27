import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# Read notebook for topics
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()

guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

blocks = []
current_block = None
total_topics = 0

for line in lines:
    text = re.sub(r'<[^>]+>', '', line).strip()
    
    # Block Header
    block_match = re.search(r'###\s*(BLOCK\s+\d+\s*[—\-]\s*[^\(]+)(?:\s*\((.*?)\))?', text)
    if block_match:
        block_title = block_match.group(1).strip()
        week_badge = block_match.group(2).strip() if block_match.group(2) else ""
        current_block = {"title": block_title, "badge": week_badge, "items": []}
        blocks.append(current_block)
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

# Build new HTML
css = """
<style>
/* Ultra Premium Checklist Redesign */
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
    background: linear-gradient(135deg, var(--text-1), var(--text-3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.tracker-hero p {
    font-size: 1.1rem;
    color: var(--text-3);
    max-width: 600px;
    margin: 0 auto;
}

.tracker-card {
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    backdrop-filter: blur(20px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.dark .tracker-card {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.tracker-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}
.tracker-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--brand), #ff9a66);
    opacity: 0.8;
}

.block-header-new {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 1rem;
}
.block-title-new {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-1);
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0;
}
.block-title-new .icon-box {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(255, 94, 0, 0.1);
    color: var(--brand);
    display: flex;
    align-items: center;
    justify-content: center;
}
.block-badge-new {
    background: rgba(255, 94, 0, 0.1);
    color: var(--brand);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    border: 1px solid rgba(255, 94, 0, 0.2);
}

.task-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.task-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 12px 16px;
    border-radius: 12px;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    position: relative;
}
.task-item:hover {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.05);
}
.task-item.subtopic {
    margin-left: 2.5rem;
}
.task-item.subtopic::before {
    content: '';
    position: absolute;
    left: -1rem;
    top: -10px;
    bottom: 50%;
    width: 2px;
    background: rgba(255, 255, 255, 0.1);
    border-bottom-left-radius: 6px;
}
.task-item.subtopic::after {
    content: '';
    position: absolute;
    left: -1rem;
    top: 50%;
    width: 1rem;
    height: 2px;
    background: rgba(255, 255, 255, 0.1);
}

.task-checkbox-label {
    display: contents;
    cursor: pointer;
}
.task-checkbox {
    display: none;
}
.task-custom-check {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid var(--text-4);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
    margin-top: 2px;
    background: transparent;
}
.task-checkbox:checked + .task-custom-check {
    background: var(--brand);
    border-color: var(--brand);
    box-shadow: 0 0 12px rgba(255, 94, 0, 0.4);
}
.task-checkbox:checked + .task-custom-check::after {
    content: '\\2713';
    color: white;
    font-size: 14px;
    font-weight: 900;
}

.task-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}
.task-title {
    font-size: 0.95rem;
    color: var(--text-1);
    font-weight: 500;
    line-height: 1.5;
    transition: color 0.2s;
}
.task-item.subtopic .task-title {
    font-size: 0.9rem;
    color: var(--text-2);
}
.task-checkbox:checked ~ .task-content .task-title {
    color: var(--text-4);
    text-decoration: line-through;
}
.task-num {
    color: var(--brand);
    font-weight: 700;
    margin-right: 6px;
}

/* Floating Progress Bar */
.floating-progress {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(20, 20, 20, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 100px;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05) inset;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    z-index: 1000;
    width: 90%;
    max-width: 600px;
}
.fp-stats {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
}
.fp-text {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
}
.fp-text span {
    color: var(--text-1);
}
.fp-bar-bg {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    overflow: hidden;
}
.fp-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--brand), #ff9a66);
    border-radius: 4px;
    width: 0%;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 10px var(--brand-glow);
}
.fp-save-btn {
    background: var(--brand);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 100px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
}
.fp-save-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px var(--brand-glow);
}
</style>
"""

blocks_html = ""
for i, block in enumerate(blocks):
    if not block["items"]: continue
    
    badge_html = f'<span class="block-badge-new">{block["badge"]}</span>' if block["badge"] else ""
    items_html = ""
    for item in block["items"]:
        is_sub = "subtopic" if item["type"] == "subtopic" else "topic"
        prefix = f"<span class='task-num'>{item['id']}.</span>" if is_sub == "topic" else ""
        
        items_html += f"""
        <label class="task-item {is_sub}">
            <input type="checkbox" class="task-checkbox" id="topic-{item['id']}">
            <div class="task-custom-check"></div>
            <div class="task-content">
                <span class="task-title">{prefix}{item['text']}</span>
            </div>
        </label>
        """
        
    blocks_html += f"""
    <div class="tracker-card">
        <div class="block-header-new">
            <h3 class="block-title-new">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                </div>
                {block['title']}
            </h3>
            {badge_html}
        </div>
        <div class="task-list">
            {items_html}
        </div>
    </div>
    """

new_checkin_content = f"""
        {css}
        <div class="checklist-master-container" id="checklist-master">
            <div class="tracker-hero">
                <h1>Roadmap Tracker</h1>
                <p>Master every topic step-by-step. Track your progress across all learning blocks and technical modules.</p>
            </div>
            
            <div class="blocks-container">
                {blocks_html}
            </div>
        </div>
        
        <div class="floating-progress">
            <div class="fp-stats">
                <div class="fp-text">
                    Progress <span id="fp-count">0 / {total_topics}</span>
                </div>
                <div class="fp-bar-bg">
                    <div class="fp-bar-fill" id="fp-bar"></div>
                </div>
            </div>
            <button class="fp-save-btn">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                Save
            </button>
        </div>
        
        <script>
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
            }});
            
            // Sync with local storage for amazing UX
            document.querySelectorAll('.task-checkbox').forEach(cb => {{
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

def replace_checklist(html):
    # The previous checklist was placed immediately after `<div class="dashboard"...>`
    # and replaced everything before `<div class="dashboard-header-row" style="margin-top: 2rem;">\n      <div class="dashboard-title-area">\n        <h2>Interview Notes Notebook</h2>`
    
    # We will use regex to find everything from `<style>\n/* Premium Checklist UI */` to `</script>`
    # OR we can just locate `<!-- Checkin start -->` if we didn't add it... wait, we didn't add comments.
    
    # Let's search for `<div class="dashboard"`
    start_tag = '<div class="dashboard"'
    start_idx = html.find(start_tag)
    if start_idx == -1: return html
    
    # find where the dashboard opening div ends
    end_of_start_tag = html.find('>', start_idx) + 1
    
    # Find where the Interview Notes Notebook section starts
    notes_start = html.find('<div class="dashboard-header-row" style="margin-top: 2rem;">')
    if notes_start == -1: return html
    
    return html[:end_of_start_tag] + new_checkin_content + html[notes_start:]


for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            html = f.read()
        
        new_html = replace_checklist(html)
        
        with open(path, "w") as f:
            f.write(new_html)

print("Completely redesigned tracking page with ultra premium layout.")
