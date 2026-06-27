import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

html_file = os.path.join(FRONTEND, "daily-checkin.html")
if os.path.exists(html_file):
    with open(html_file, "r") as f:
        html_content = f.read()

    # 1. Update Tracker Block Numbers to NOT be colourful
    # Find: <div class="acc-block-num" style="background:#XXXXXX">
    # Replace with: <div class="acc-block-num" style="background:var(--text-1); color:var(--bg);">
    html_content = re.sub(
        r'<div class="acc-block-num" style="background:#[a-fA-F0-9]+">',
        r'<div class="acc-block-num" style="background:var(--text-1); color:var(--bg);">',
        html_content
    )

    with open(html_file, "w") as f:
        f.write(html_content)
    print("daily-checkin.html patched.")
else:
    print("daily-checkin.html not found.")
