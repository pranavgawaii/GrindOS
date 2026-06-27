import os

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

files_to_fix = ["htmlfresher.html", "daily-checkin.html"]

for filename in files_to_fix:
    filepath = os.path.join(FRONTEND, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add clerk.js to <head> if missing
    if 'auth/clerk.js' not in content:
        content = content.replace('</head>', '  <script src="auth/clerk.js"></script>\n</head>')
        
    # 2. Add script.js to bottom of <body> if missing
    if 'assets/script.js' not in content:
        content = content.replace('</body>', '  <script src="assets/script.js?v=21"></script>\n</body>')

    with open(filepath, 'w') as f:
        f.write(content)
        
    print(f"Fixed {filename}")
