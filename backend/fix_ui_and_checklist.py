import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# 1. First, append mobile nav css to style.css if it doesn't exist
style_css_path = os.path.join(FRONTEND, "assets", "style.css")
with open(style_css_path, "r") as f:
    style_css = f.read()

mobile_css = """
/* Mobile Navigation */
.mobile-bottom-nav {
  display: none;
}
@media (max-width: 768px) {
  .mobile-bottom-nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--surface-1);
    border-top: 1px solid var(--border);
    padding: 0.5rem 0;
    z-index: 1000;
  }
  .mobile-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--text-2);
    text-decoration: none;
    font-size: 0.75rem;
    gap: 0.25rem;
  }
  .mobile-nav-icon svg {
    width: 24px;
    height: 24px;
  }
  .mobile-nav-item.active {
    color: var(--brand);
  }
  body {
    padding-bottom: 70px; /* space for mobile nav */
  }
}

.checklist-container {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--surface-2);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.checklist-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background 0.2s;
}

.checklist-item:hover {
    background: var(--surface-1);
}

.checklist-item input[type="checkbox"] {
    width: 18px;
    height: 18px;
    margin-top: 2px;
    cursor: pointer;
    accent-color: var(--brand);
}

.checklist-item label {
    cursor: pointer;
    color: var(--text-1);
    font-size: 0.95rem;
    line-height: 1.4;
    user-select: none;
}
.checklist-item input:checked + label {
    text-decoration: line-through;
    color: var(--text-3);
}

/* Custom Scrollbar for Checklist */
.checklist-container::-webkit-scrollbar {
    width: 6px;
}
.checklist-container::-webkit-scrollbar-track {
    background: transparent;
}
.checklist-container::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}
.checklist-container::-webkit-scrollbar-thumb:hover {
    background: var(--text-4);
}
"""
if ".mobile-bottom-nav" not in style_css:
    with open(style_css_path, "a") as f:
        f.write("\n" + mobile_css)

# 2. Extract topics from htmlfresher.html
htmlfresher_path = os.path.join(FRONTEND, "htmlfresher.html")
with open(htmlfresher_path, "r") as f:
    content = f.read()

# The topics are inside tab-guide, starting with digits.
guide_match = re.search(r'<div id="tab-guide".*?(<div class="ruled">.*?</div>)', content, flags=re.DOTALL)
checklist_items_html = ""
if guide_match:
    guide_html = guide_match.group(1)
    # find lines with numbers
    lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_html)
    
    topics = []
    for line in lines:
        text = re.sub(r'<[^>]+>', '', line) # remove html tags
        match = re.match(r'^(\d+)\.\s+(.*)', text)
        if match:
            topics.append((match.group(1), match.group(2)))
            
    # Generate checklist html
    for i, (num, text) in enumerate(topics):
        checklist_items_html += f"""
        <div class="checklist-item">
            <input type="checkbox" id="topic-{num}">
            <label for="topic-{num}"><b>{num}.</b> {text}</label>
        </div>
        """

# 3. Replace the textarea section in htmlfresher.html and daily-checkin.html
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
        </script>
"""

import sys
def replace_form(html_content):
    # Regex to find the whole flex block containing the textarea and replace it
    pattern = r'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">\s*<div style="width: 40px.*?</button>\s*</div>'
    return re.sub(pattern, new_checkin_content, html_content, flags=re.DOTALL)

with open(htmlfresher_path, "w") as f:
    f.write(replace_form(content))

daily_checkin_path = os.path.join(FRONTEND, "daily-checkin.html")
with open(daily_checkin_path, "r") as f:
    daily_content = f.read()

with open(daily_checkin_path, "w") as f:
    f.write(replace_form(daily_content))

print(f"Replaced Check-In form with checklist of {len(topics)} topics in both files.")
