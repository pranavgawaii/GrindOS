import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

def fix_navbar(filepath, active_class_name):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        html = f.read()

    # Find the topbar-nav block
    nav_pattern = r'<nav class="topbar-nav">(.*?)</nav>'
    nav_match = re.search(nav_pattern, html, flags=re.DOTALL)
    if not nav_match: return
    
    nav_content = nav_match.group(1)
    
    # Remove 'active' from all links in this nav block
    nav_content = re.sub(r'class="([^"]*?)\s*active\s*([^"]*?)"', r'class="\1 \2"', nav_content)
    nav_content = re.sub(r'class="active\s*([^"]*?)"', r'class="\1"', nav_content)
    nav_content = re.sub(r'class="([^"]*?)\s*active"', r'class="\1"', nav_content)
    nav_content = nav_content.replace(' class="active"', '')
    
    # Clean up multiple spaces in class names that might result from removal
    nav_content = re.sub(r'class="\s+', 'class="', nav_content)
    nav_content = re.sub(r'\s+"', '"', nav_content)
    
    # Add 'active' to the correct link
    # Look for class="<active_class_name>" and append " active"
    target_pattern = rf'class="{active_class_name}"'
    nav_content = re.sub(target_pattern, f'class="{active_class_name} active"', nav_content)
    
    # Also handle if there are other classes e.g. class="tracker-nav something"
    target_pattern_complex = rf'class="{active_class_name} ([^"]+)"'
    nav_content = re.sub(target_pattern_complex, f'class="{active_class_name} \\1 active"', nav_content)
    
    # Replace the old nav block with the new one
    new_html = html[:nav_match.start(1)] + nav_content + html[nav_match.end(1):]
    
    with open(filepath, 'w') as f:
        f.write(new_html)
    print(f"Fixed navbar in {os.path.basename(filepath)}")

# 1. Fix htmlfresher.html to highlight Tracker
fix_navbar(os.path.join(FRONTEND, "htmlfresher.html"), "tracker-nav")

# 2. Fix daily-checkin.html to highlight Check In
fix_navbar(os.path.join(FRONTEND, "daily-checkin.html"), "checkin-nav")

# 3. Fix interview_qa.html to highlight Tracker
fix_navbar(os.path.join(FRONTEND, "interview_qa.html"), "tracker-nav")
