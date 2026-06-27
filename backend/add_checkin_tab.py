import os
import glob
import re
import shutil

FRONTEND_DIR = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend"

# 1. Copy dashboard to daily-checkin
shutil.copy(os.path.join(FRONTEND_DIR, "dashboard.html"), os.path.join(FRONTEND_DIR, "daily-checkin.html"))

# 2. Modify daily-checkin.html content
with open(os.path.join(FRONTEND_DIR, "daily-checkin.html"), "r") as f:
    content = f.read()

# Make the checkin tab active, remove active from others
content = content.replace('class="learn-nav active"', 'class="learn-nav"')

new_dashboard_content = """  <div class="dashboard">
    <div class="dashboard-header-row">
      <div class="dashboard-title-area">
        <h2>Daily Check In</h2>
        <p>Log your daily progress, learnings, and any blockers here.</p>
      </div>
    </div>
    <div style="max-width: 800px; margin-top: 2rem;">
        <div class="check-in-form" style="display: flex; flex-direction: column; gap: 1rem; width: 100%;">
            <textarea placeholder="What did you learn or practice today?" style="width: 100%; min-height: 150px; padding: 1rem; border: 1px solid var(--border); border-radius: 8px; background: var(--surface-1); color: var(--text-primary); font-family: inherit; resize: vertical; font-size: 15px;"></textarea>
            <button style="align-self: flex-start; padding: 0.75rem 1.5rem; background-color: var(--brand); color: var(--surface-1); border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 15px;">Submit Check-in</button>
        </div>
    </div>
  </div>"""

# Replace the inner dashboard div
content = re.sub(r'<div class="dashboard">.*?</div>\s*<script', new_dashboard_content + '\n\n<script', content, flags=re.DOTALL)

with open(os.path.join(FRONTEND_DIR, "daily-checkin.html"), "w") as f:
    f.write(content)

# 3. Update navs in all HTML files
mobile_svg = """<svg viewBox="0 0 24 24" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>"""
mobile_svg_check = """<svg viewBox="0 0 24 24" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="currentColor"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>"""

for root, _, files in os.walk(FRONTEND_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                html = f.read()
                
            # If already added, skip
            if 'class="checkin-nav"' in html:
                continue

            # Determine prefix from the resume-builder link
            match = re.search(r'<a href="([^"]*)resume-builder\.html"[^>]*>Resume</a>', html)
            prefix = match.group(1) if match else ""
            
            # Replace topbar
            topbar_replace = f'Resume</a>\n      <a href="{prefix}daily-checkin.html" class="checkin-nav">Check In</a>'
            html = re.sub(r'Resume</a>', topbar_replace, html, count=1)
            
            # Replace mobile nav if present
            if 'id="mnav-resume"' in html:
                mobile_addition = f"""    </a>
    <a href="{prefix}daily-checkin.html" class="mobile-nav-item" id="mnav-checkin">
      <span class="mobile-nav-icon">
        {mobile_svg_check}
      </span>
      <span>Check In</span>
"""
                # find the closing </a> for the resume nav
                html = re.sub(r'(id="mnav-resume".*?<span>Resume</span>\s*)</a>', r'\1' + mobile_addition + '    </a>', html, flags=re.DOTALL)
            
            # If this is the daily-checkin file, mark it active
            if file == "daily-checkin.html":
                html = html.replace('class="checkin-nav"', 'class="checkin-nav active"')
                html = html.replace('id="mnav-checkin"', 'id="mnav-checkin" class="mobile-nav-item active"')

            with open(path, "w") as f:
                f.write(html)
            print(f"Updated nav in {file}")

