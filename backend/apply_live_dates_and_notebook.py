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
        # Remove the "BLOCK X -" part for the title to be cleaner
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

# 2. Parse Roadmap for tips/tricks/resources/dates
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
    
    # Extract duration in days (e.g. 10 days)
    dur_match = re.search(r'>(\d+)\s*days<', rm_block)
    if dur_match: 
        target_block["days"] = int(dur_match.group(1))
    
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
    
    # Distribute days across items
    num_items = len(block["items"])
    if num_items > 0:
        days_per_item = block["days"] / num_items
        for i, item in enumerate(block["items"]):
            item_date = block_start_date + timedelta(days=(i+1)*days_per_item)
            item["due_date"] = item_date
            
    # Move current date forward for next block
    current_date = block["end_date"]


# 4. Generate New HTML for Tracker
css = """
<style>
/* Live Tracking Accordion Checklist */
.checklist-master-container { max-width: 900px; margin: 0 auto; padding: 0 1rem; padding-bottom: 120px; }
.tracker-hero { text-align: center; margin-bottom: 3rem; padding: 2rem 0; }
.tracker-hero h1 { font-size: 2.2rem; font-weight: 800; color: var(--text-1); margin-bottom: 0.5rem; }
.tracker-hero p { font-size: 1.1rem; color: var(--text-3); max-width: 600px; margin: 0 auto; }

.acc-card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 1.5rem; overflow: hidden; transition: border-color 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.acc-card:hover { border-color: var(--border-strong); }
.acc-header { padding: 1.25rem 1.5rem; background: var(--surface-2); display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; }
.acc-header-left { display: flex; flex-direction: column; gap: 4px; }
.acc-title { font-size: 1.15rem; font-weight: 700; color: var(--text-1); letter-spacing: 0.02em; }
.acc-date-pill { display: inline-flex; align-items: center; gap: 6px; font-size: 0.8rem; color: var(--brand); font-weight: 600; padding: 4px 10px; background: rgba(255, 94, 0, 0.1); border-radius: 20px; border: 1px solid rgba(255, 94, 0, 0.2); width: fit-content; margin-top: 4px;}
.acc-chevron { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); color: var(--text-3); }
.acc-card.open .acc-chevron { transform: rotate(180deg); }

.acc-body { display: none; padding: 1.5rem; border-top: 1px solid var(--border); }
.acc-card.open .acc-body { display: block; }

.task-list { display: flex; flex-direction: column; gap: 4px; margin-bottom: 2rem; }
.task-item { display: flex; align-items: flex-start; gap: 14px; padding: 10px 14px; border-radius: 8px; cursor: pointer; transition: background 0.2s; }
.task-item:hover { background: var(--surface-0); }
.task-item.subtopic { margin-left: 2.5rem; }
.task-checkbox { display: none; }
.task-custom-check { width: 20px; height: 20px; border-radius: 5px; border: 2px solid var(--text-4); display: flex; align-items: center; justify-content: center; margin-top: 2px; flex-shrink: 0; }
.task-checkbox:checked + .task-custom-check { background: var(--text-1); border-color: var(--text-1); }
.task-checkbox:checked + .task-custom-check::after { content: '\\2713'; color: var(--bg); font-size: 14px; font-weight: bold; }
.task-content { flex: 1; display: flex; align-items: center; justify-content: space-between; gap: 1rem;}
.task-title { font-size: 0.95rem; color: var(--text-1); line-height: 1.5; }
.task-checkbox:checked ~ .task-content .task-title { color: var(--text-4); text-decoration: line-through; }
.task-num { font-weight: 700; margin-right: 6px; color: var(--brand); }
.task-due { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; white-space: nowrap; }

.acc-meta { display: flex; flex-direction: column; gap: 1.25rem; padding-top: 1.5rem; border-top: 1px solid var(--border-light); }
.meta-section h4 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.75rem; }
.info-box { padding: 1rem; border-radius: 8px; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0.5rem; }
.box-note { background: rgba(245, 166, 35, 0.1); border: 1px solid rgba(245, 166, 35, 0.2); color: var(--text-1); }
.box-note b { color: #f5a623; }
.box-tip { background: rgba(46, 213, 115, 0.1); border: 1px solid rgba(46, 213, 115, 0.2); color: var(--text-1); }
.box-tip b { color: #2ed573; }
.res-links { display: flex; flex-direction: column; gap: 8px; }
.res-links a { display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: var(--surface-0); border: 1px solid var(--border); border-radius: 8px; color: var(--text-1); text-decoration: none; font-size: 0.9rem; transition: border-color 0.2s; }
.res-links a:hover { border-color: var(--text-3); }

/* Floating Progress Bar */
.floating-progress { position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); background: var(--surface-2); border: 1px solid var(--border-strong); border-radius: 100px; padding: 12px 24px; display: flex; align-items: center; gap: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); z-index: 1000; width: 90%; max-width: 600px; backdrop-filter: blur(10px); }
.fp-stats { flex: 1; }
.fp-text { font-size: 0.85rem; font-weight: 600; color: var(--text-2); margin-bottom: 6px; display: flex; justify-content: space-between;}
.fp-bar-bg { width: 100%; height: 6px; background: var(--surface-0); border-radius: 3px; overflow: hidden; }
.fp-bar-fill { height: 100%; background: var(--text-1); border-radius: 3px; width: 0%; transition: width 0.3s; }
.fp-save-btn { background: var(--text-1); color: var(--bg); border: none; padding: 10px 20px; border-radius: 100px; font-weight: 600; cursor: pointer; }
</style>
"""

blocks_html = ""
for block in blocks_data:
    if not block["items"]: continue
    
    items_html = ""
    for item in block["items"]:
        is_sub = "subtopic" if item["type"] == "subtopic" else "topic"
        prefix = f"<span class='task-num'>{item['id']}.</span>" if is_sub == "topic" else ""
        date_str = item["due_date"].strftime("%b %d")
        
        items_html += f"""
        <label class="task-item {is_sub}">
            <input type="checkbox" class="task-checkbox" id="topic-{item['id']}">
            <div class="task-custom-check"></div>
            <div class="task-content">
                <span class="task-title">{prefix}{item['text']}</span>
                <span class="task-due">{date_str}</span>
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
                <p>Live progress tracking. We calculated your specific deadlines starting from today.</p>
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
                const isOpen = el.classList.contains('open');
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

# Premium Notebook CSS Override
notebook_css = """
<style>
/* Premium Digital Notebook Redesign */
.dashboard-header-row h2 { font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; }
.dashboard-header-row p { font-size: 1.05rem; color: var(--text-2); }
.nb-wrap { background: transparent !important; }
.nb-tabs { border-bottom: 1px solid var(--border) !important; margin-bottom: 1.5rem !important; gap: 8px !important; }
.nb-tab { border: 1px solid transparent !important; border-radius: 8px 8px 0 0 !important; background: transparent !important; font-weight: 600 !important; padding: 12px 20px !important; transition: all 0.2s !important; color: var(--text-3) !important; }
.nb-tab:hover { color: var(--text-1) !important; background: var(--surface-1) !important; }
.nb-tab.active { background: var(--surface-2) !important; color: var(--brand) !important; border-color: var(--border) !important; border-bottom-color: var(--surface-2) !important; margin-bottom: -1px !important; }
.page-frame { background: var(--surface-1) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; box-shadow: 0 4px 30px rgba(0,0,0,0.1) !important; padding: 2.5rem !important; }
.page-top { border-bottom: 1px solid var(--border-light) !important; padding-bottom: 1.5rem !important; margin-bottom: 1.5rem !important; }
.page-subject { font-weight: 700 !important; letter-spacing: 0.05em !important; font-size: 0.85rem !important; text-transform: uppercase !important; }
.page-title { font-size: 1.8rem !important; font-weight: 800 !important; color: var(--text-1) !important; margin-top: 8px !important; }
.ruled { background: transparent !important; background-image: none !important; padding: 0 !important; }
.line { border-bottom: none !important; padding: 4px 0 !important; margin-bottom: 4px !important; }
.line-num { display: none !important; }
.line-content { color: var(--text-1) !important; font-family: 'Inter', system-ui, sans-serif !important; font-size: 1.05rem !important; line-height: 1.7 !important; }
.hl-purple, .hl-blue, .hl-coral, .hl-teal { font-weight: 700 !important; color: var(--brand) !important; font-size: 1.1rem !important; display: inline-block !important; margin-top: 1rem !important; }
.arrow { color: var(--brand-glow) !important; margin-right: 12px !important; font-weight: bold !important; font-size: 1.2rem !important;}
.indent { padding-left: 2rem !important; }
.sticky { background: rgba(255, 94, 0, 0.05) !important; border: 1px solid rgba(255, 94, 0, 0.2) !important; border-radius: 8px !important; box-shadow: none !important; transform: none !important; margin-top: 2rem !important; padding: 1.5rem !important; }
.sticky-title { font-size: 1.1rem !important; font-weight: 700 !important; color: var(--brand) !important; margin-bottom: 8px !important; }
.warn-box { background: rgba(255, 60, 60, 0.1) !important; border: 1px solid rgba(255, 60, 60, 0.2) !important; border-radius: 8px !important; padding: 1.5rem !important; margin-top: 2rem !important; color: var(--text-1) !important; }
</style>
"""


def apply_updates(html):
    # Replace Tracker
    start_tag = '<div class="checklist-master-container"'
    start_idx = html.find(start_tag)
    if start_idx != -1:
        end_idx = html.find('</script>', start_idx) + len('</script>')
        html = html[:start_idx] + new_tracker_html + html[end_idx:]
    
    # Filter Notebook content
    # Remove OOP tab
    html = re.sub(r'<div class="nb-tab[^>]*>OOP page</div>', '', html)
    html = re.sub(r'<div id="tab-oop" class="nb-page.*?</div>\s*</div>\s*</div>\s*(?=<div id="tab-os")', '', html, flags=re.DOTALL)
    
    # Make OS tab active since OOP is gone
    html = re.sub(r'<div class="nb-tab" onclick="switchTab\(\'os\'\)">', r'<div class="nb-tab active" onclick="switchTab(\'os\')">', html)
    html = re.sub(r'<div id="tab-os" class="nb-page">', r'<div id="tab-os" class="nb-page active">', html)
    
    # Inject Notebook CSS Override right before the Notebook starts
    nb_start = html.find('<div class="nb-wrap">')
    if nb_start != -1:
        html = html[:nb_start] + notebook_css + html[nb_start:]
    
    return html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            html = f.read()
        new_html = apply_updates(html)
        with open(path, "w") as f:
            f.write(new_html)

print("Live Dates applied and Notebook redesigned & filtered!")
