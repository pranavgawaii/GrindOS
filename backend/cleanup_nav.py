import os
import re
import shutil

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend"

# 1. Copy daily-checkin.html to tracker.html
src_file = os.path.join(ROOT, "daily-checkin.html")
dest_file = os.path.join(ROOT, "tracker.html")
if os.path.exists(src_file):
    shutil.copy2(src_file, dest_file)

# 2. Iterate over all HTML files and remove Check In nav link
def process_html_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    # Remove the Check In link
    content = re.sub(r'<a href="[^"]*daily-checkin\.html"[^>]*>Check In</a>', '', content)
    
    # Fix the active state for tracker.html
    if filepath.endswith("tracker.html"):
        content = re.sub(r'class="tracker-nav[^"]*"', 'class="tracker-nav active"', content)
        content = re.sub(r'class="checkin-nav[^"]*"', 'class="checkin-nav"', content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(ROOT):
    for file in files:
        if file.endswith('.html'):
            process_html_file(os.path.join(root, file))

print("Cleanup complete!")
