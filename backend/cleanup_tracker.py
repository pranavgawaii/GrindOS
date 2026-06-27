import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

def cleanup_html(html):
    # The old Daily Check-In header starts like this:
    # <div class="dashboard-header-row" style="margin-top: 2rem;">
    #   <div class="dashboard-title-area">
    #     <h2>Daily Check-In</h2>
    
    # We want to remove everything from this `dashboard-header-row` until the start of the next `dashboard-header-row`
    # which is the "Interview Notes Notebook" section.
    
    pattern = r'<div class="dashboard-header-row"[^>]*>\s*<div class="dashboard-title-area">\s*<h2>Daily Check-In</h2>.*?(?=<div class="dashboard-header-row"[^>]*>\s*<div class="dashboard-title-area">\s*<h2>Interview Notes Notebook</h2>)'
    
    new_html = re.sub(pattern, '', html, flags=re.DOTALL)
    return new_html

for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            html = f.read()
            
        new_html = cleanup_html(html)
        
        with open(path, "w") as f:
            f.write(new_html)

print("Cleanup script executed!")
