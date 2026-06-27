import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()

# Extract lines in tab-guide
guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

blocks = []
current_block = None
total_topics = 0

for line in lines:
    text = re.sub(r'<[^>]+>', '', line).strip()
    
    # Match Block Header: ### BLOCK 1 — PROGRAMMING FOUNDATION (Week 1-2)
    # The (Week X) part might not exist or might be structured differently
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

print(f"Parsed {len(blocks)} blocks with a total of {total_topics} items.")

css = """
<style>
/* Premium Checklist UI */
.block-group {
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface-1);
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.block-header {
    padding: 1.25rem 1.5rem;
    background: var(--surface-2);
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 10;
}
.block-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--brand);
    margin: 0;
    letter-spacing: 0.02em;
}
.block-badge {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 10px;
    background: var(--brand-light);
    color: var(--brand);
    border-radius: 20px;
    border: 1px solid var(--brand-glow);
}
.block-items {
    padding: 0.75rem 0;
}
.chk-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
    transition: background 0.2s;
    position: relative;
}
.chk-item:hover {
    background: var(--surface-2);
}
.chk-item.subtopic {
    padding-left: 3.5rem;
    position: relative;
}
.chk-item.subtopic::before {
    content: '';
    position: absolute;
    left: 2rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--border);
}
.chk-item.subtopic::after {
    content: '';
    position: absolute;
    left: 2rem;
    top: 1.25rem;
    width: 1rem;
    height: 2px;
    background: var(--border);
}
.chk-input {
    width: 20px;
    height: 20px;
    margin-top: 2px;
    cursor: pointer;
    accent-color: var(--brand);
    position: relative;
    z-index: 2;
}
.chk-label {
    cursor: pointer;
    color: var(--text-1);
    font-size: 0.95rem;
    line-height: 1.5;
    user-select: none;
    flex: 1;
}
.chk-label b {
    color: var(--text-1);
    margin-right: 4px;
}
.chk-item.subtopic .chk-label {
    font-size: 0.9rem;
    color: var(--text-2);
}
.chk-input:checked + .chk-label {
    text-decoration: line-through;
    color: var(--text-4);
}
.checklist-wrapper {
    max-height: 600px;
    overflow-y: auto;
    border-radius: 12px;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: var(--brand) transparent;
}
.checklist-wrapper::-webkit-scrollbar {
    width: 6px;
}
.checklist-wrapper::-webkit-scrollbar-track {
    background: transparent;
}
.checklist-wrapper::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}
.checklist-wrapper::-webkit-scrollbar-thumb:hover {
    background: var(--brand);
}
</style>
"""

blocks_html = ""
for block in blocks:
    if not block["items"]: continue
    
    badge_html = f'<span class="block-badge">{block["badge"]}</span>' if block["badge"] else ""
    items_html = ""
    for item in block["items"]:
        is_sub = "subtopic" if item["type"] == "subtopic" else "topic"
        prefix = f"<b>{item['id']}.</b> " if is_sub == "topic" else ""
        
        items_html += f"""
        <div class="chk-item {is_sub}">
            <input type="checkbox" class="chk-input" id="topic-{item['id']}">
            <label class="chk-label" for="topic-{item['id']}">{prefix}{item['text']}</label>
        </div>
        """
        
    blocks_html += f"""
    <div class="block-group">
        <div class="block-header">
            <h3 class="block-title">{block['title']}</h3>
            {badge_html}
        </div>
        <div class="block-items">
            {items_html}
        </div>
    </div>
    """

new_checkin_content = f"""
        {css}
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.5rem;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: var(--brand-light); display: flex; align-items: center; justify-content: center; color: var(--brand); box-shadow: 0 4px 12px var(--brand-glow);">
                <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.3rem; color: var(--text-1); letter-spacing: -0.02em;">Mastery Checklist</h3>
                <p style="margin: 0; font-size: 0.9rem; color: var(--text-3); margin-top: 2px;">Track your sequential progress through the GrindOS Complete Guide.</p>
            </div>
        </div>
        
        <div class="checklist-wrapper" id="daily-checklist">
            {blocks_html}
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="font-size: 0.9rem; color: var(--text-2); font-weight: 500;" id="progress-text">0 / {total_topics} Topics Completed</div>
                <div style="width: 200px; height: 6px; background: var(--surface-2); border-radius: 3px; overflow: hidden;">
                    <div id="progress-bar" style="width: 0%; height: 100%; background: var(--brand); border-radius: 3px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            <button id="submit-checkin" style="padding: 0.75rem 2.5rem; background: var(--brand-gradient); color: white; border: none; border-radius: 99px; cursor: pointer; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px var(--brand-glow); transition: all 0.2s; display: flex; align-items: center; gap: 8px;">
                <span>Sync Progress</span>
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                  <path d="M9 11l3 3L22 4"></path>
                </svg>
            </button>
        </div>
        
        <script>
            function updateProgress() {{
                const checkboxes = document.querySelectorAll('#daily-checklist .chk-input');
                const checked = document.querySelectorAll('#daily-checklist .chk-input:checked').length;
                const total = checkboxes.length;
                
                document.getElementById('progress-text').textContent = checked + " / " + total + " Topics Completed";
                const pct = total === 0 ? 0 : (checked / total) * 100;
                document.getElementById('progress-bar').style.width = pct + "%";
            }}
            
            document.querySelectorAll('#daily-checklist .chk-input').forEach(cb => {{
                cb.addEventListener('change', updateProgress);
            }});
            
            if (document.readyState === 'complete') updateProgress();
            else window.addEventListener('DOMContentLoaded', updateProgress);
        </script>
"""

def replace_checklist(html):
    # Regex to replace the entire previous Check-In section
    # The previous one started with: <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
    # And ended with the script block.
    start_tag = '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">'
    end_tag = '</script>'
    
    if start_tag in html:
        start_idx = html.find(start_tag)
        # Find the next </div>\n    </div> after the script
        end_idx = html.find('</script>', start_idx) + len('</script>')
        return html[:start_idx] + new_checkin_content + html[end_idx:]
    return html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    with open(path, "r") as f:
        html = f.read()
    with open(path, "w") as f:
        f.write(replace_checklist(html))

print(f"Redesigned premium grouped checklist added to {len(blocks)} blocks!")
