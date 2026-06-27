import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
CHECKIN_SYS = os.path.join(ROOT, "grindos_checkin_system.html")
TRACKER_HTML = os.path.join(FRONTEND, "tracker.html")
STYLE_CSS = os.path.join(FRONTEND, "assets", "style.css")

with open(CHECKIN_SYS, 'r') as f:
    sys_content = f.read()

# Extract styles
style_match = re.search(r'<style>(.*?)</style>', sys_content, re.DOTALL)
sys_styles = style_match.group(1).strip() if style_match else ""

# Extract HTML content
html_match = re.search(r'<div class="w">(.*?)</div>\s*<script>', sys_content, re.DOTALL)
sys_html = '<div class="w">\n' + html_match.group(1).strip() + '\n</div>' if html_match else ""

# Extract JS
js_match = re.search(r'<script>(.*?)</script>', sys_content, re.DOTALL)
sys_js = js_match.group(1).strip() if js_match else ""

# Modify tracking HTML
with open(TRACKER_HTML, 'r') as f:
    tracker = f.read()

# Locate the hero section to insert AFTER
hero_end = tracker.find('</div>\n  <div class="metrics-grid">')
if hero_end != -1:
    # We want to keep the hero section, so find the end of it
    pass
else:
    print("Could not find metrics-grid")

# Let's replace everything from <div class="metrics-grid"> up to the Notebook section
# The notebook section starts with <style>\n    /* Notebook specific styles */
notebook_start = tracker.find('<style>\n    /* Notebook specific styles */')

if hero_end != -1 and notebook_start != -1:
    new_tracker = tracker[:hero_end + 7] + "\n" + sys_html + "\n  </div>\n" + tracker[notebook_start:]
    
    # Inject JS at the bottom
    if '<script src="assets/script.js?v=21"></script>' in new_tracker:
        new_tracker = new_tracker.replace(
            '<script src="assets/script.js?v=21"></script>',
            f'<script>\n{sys_js}\n</script>\n<script src="assets/script.js?v=21"></script>'
        )
    
    with open(TRACKER_HTML, 'w') as f:
        f.write(new_tracker)
    print("Injected HTML and JS into tracker.html")
else:
    print("Failed to find insertion points")

# Append styles to style.css
with open(STYLE_CSS, 'r') as f:
    css = f.read()
if "/* GrindOS Check In system */" not in css:
    with open(STYLE_CSS, 'a') as f:
        f.write("\n/* GrindOS Check In system */\n" + sys_styles)
    print("Appended CSS to style.css")
