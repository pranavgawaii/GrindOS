import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
DASHBOARD = os.path.join(FRONTEND, "dashboard.html")
CHECKIN_SYS = os.path.join(ROOT, "grindos_checkin_system.html")
NOTEBOOK = os.path.join(ROOT, "interview_notes_notebook.html")
TRACKER = os.path.join(FRONTEND, "tracker.html")

# 1. Get Base HTML from Dashboard
with open(DASHBOARD, 'r') as f:
    dashboard_content = f.read()

head_match = re.search(r'(<!DOCTYPE html>.*?<nav class="topbar-nav">.*?</nav>.*?</header>)', dashboard_content, re.DOTALL)
base_html = head_match.group(1)

# Fix the navbar active state
base_html = re.sub(r'class="[^"]*active[^"]*"', 'class="learn-nav"', base_html) # remove active from learn
base_html = base_html.replace('class="tracker-nav"', 'class="tracker-nav active"') # add active to tracker
base_html = base_html.replace('<title>Learn — GrindOS</title>', '<title>Tracker — GrindOS</title>')
base_html = base_html.replace('</title>', '</title>\n  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">')

# 2. Get Check In System
with open(CHECKIN_SYS, 'r') as f:
    sys_content = f.read()

qa_btn = '''
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
    <h1 style="font-size: 1.8rem; font-weight: 800; color: var(--text-1);">Roadmap Tracker</h1>
    <a href="interview_qa.html" style="display:inline-flex; align-items:center; gap:8px; background:rgba(255,94,0,0.15); border:1px solid rgba(255,94,0,0.3); color:#ff5e00; padding:8px 16px; border-radius:100px; text-decoration:none; font-weight:600; font-size:0.9rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,94,0,0.25)'" onmouseout="this.style.background='rgba(255,94,0,0.15)'">
        <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 2a10 10 0 1 0 10 10H12V2z"></path><path d="M12 12 2.1 12"></path><path d="M12 12l8.5 8.5"></path></svg>
        Interview Q&A Bank
    </a>
</div>
'''

html_match = re.search(r'<div class="w">(.*?)</div>\s*<script>', sys_content, re.DOTALL)
sys_html = '<div class="w">\n' + html_match.group(1).strip() + '\n</div>'

js_match = re.search(r'<script>(.*?)</script>', sys_content, re.DOTALL)
sys_js = js_match.group(1).strip()

# 3. Get Notebook
with open(NOTEBOOK, 'r') as f:
    nb_content = f.read()

nb_style_match = re.search(r'<style>(.*?)</style>', nb_content, re.DOTALL)
nb_style = nb_style_match.group(1).strip() if nb_style_match else ""

nb_html_match = re.search(r'<div class="nb-wrap">(.*)', nb_content, re.DOTALL)
nb_html = '<div class="nb-wrap">' + nb_html_match.group(1).strip()
nb_html = re.sub(r'<script.*?</script>', '', nb_html, flags=re.DOTALL)

# Grab the switchTab function
nb_js_match = re.search(r'<script>(.*?)</script>', nb_content, re.DOTALL)
nb_js = nb_js_match.group(1).strip() if nb_js_match else ""

# 4. Assemble
final_html = base_html + "\n<main class=\"main-content\">\n" + qa_btn + "\n" + sys_html + "\n<style>\n" + nb_style + "\n</style>\n" + nb_html + f"\n</main>\n<script>\n{sys_js}\n{nb_js}\n</script>\n<script src=\"assets/script.js?v=22\"></script>\n</body>\n</html>"

with open(TRACKER, 'w') as f:
    f.write(final_html)

print("Rebuilt tracker.html cleanly.")
