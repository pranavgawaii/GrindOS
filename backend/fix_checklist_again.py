import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

htmlfresher_path = os.path.join(FRONTEND, "htmlfresher.html")
with open(htmlfresher_path, "r") as f:
    content = f.read()

# Parse notebook directly to avoid nested div regex issues
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()
    
# Extract lines in tab-guide
guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

topics = []
for line in lines:
    text = re.sub(r'<[^>]+>', '', line) # remove html tags
    match = re.match(r'^(\d+)\.\s+(.*)', text)
    if match:
        topics.append((match.group(1), match.group(2)))

print(f"Found {len(topics)} topics!")

checklist_items_html = ""
for i, (num, text) in enumerate(topics):
    checklist_items_html += f"""
        <div class="checklist-item">
            <input type="checkbox" id="topic-{num}">
            <label for="topic-{num}"><b>{num}.</b> {text}</label>
        </div>
    """

new_checkin_content = f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--brand-light); display: flex; align-items: center; justify-content: center; color: var(--brand);">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.1rem; color: var(--text-1);">Topic Progress Tracker</h3>
                <p style="margin: 0; font-size: 0.85rem; color: var(--text-3);">Tick off the topics you have completed in the Complete Guide sequence.</p>
            </div>
        </div>
        
        <div class="checklist-container" id="daily-checklist">
            {checklist_items_html}
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 0.85rem; color: var(--text-4);" id="progress-text">0 / {len(topics)} Topics Completed</div>
            <button id="submit-checkin" style="padding: 0.75rem 2rem; background: var(--brand-gradient); color: white; border: none; border-radius: 99px; cursor: pointer; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px var(--brand-glow); transition: all 0.2s; display: flex; align-items: center; gap: 8px;">
                <span>Save Progress</span>
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            </button>
        </div>
        
        <script>
            // Basic script to update progress text
            const checkboxes = document.querySelectorAll('#daily-checklist input[type="checkbox"]');
            const progressText = document.getElementById('progress-text');
            function updateProgress() {{
                const checked = document.querySelectorAll('#daily-checklist input[type="checkbox"]:checked').length;
                progressText.textContent = checked + " / " + checkboxes.length + " Topics Completed";
            }}
            checkboxes.forEach(cb => cb.addEventListener('change', updateProgress));
            
            // Re-apply if already loaded
            if (document.readyState === 'complete') updateProgress();
        </script>
"""

def replace_checklist(html):
    pattern = r'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">\s*<div style="width: 40px.*?</div>\s*</button>\s*</div>\s*<script>.*?</script>'
    # also try matching without script if it doesn't exist
    alt_pattern = r'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">\s*<div style="width: 40px.*?</button>\s*</div>'
    
    # Let's use a simpler replacement: replace everything from the header div to the end of the script or button
    start_tag = '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">'
    end_tag = '</script>'
    
    if start_tag in html:
        start_idx = html.find(start_tag)
        # Find the next </div>\n    </div> after the button
        end_idx = html.find('</div>\n    </div>\n\n    \n    <div class="dashboard-header-row"')
        if end_idx != -1:
            return html[:start_idx] + new_checkin_content + html[end_idx:]
    
    return html

new_fresher = replace_checklist(content)
with open(htmlfresher_path, "w") as f:
    f.write(new_fresher)

daily_path = os.path.join(FRONTEND, "daily-checkin.html")
with open(daily_path, "r") as f:
    daily_content = f.read()

with open(daily_path, "w") as f:
    f.write(replace_checklist(daily_content))

print("Successfully replaced with populated checklist!")
