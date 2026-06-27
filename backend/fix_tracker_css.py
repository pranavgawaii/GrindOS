import os
import re

file_path = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/tracker.html"
with open(file_path, 'r') as f:
    content = f.read()

# Fix t-cb background
content = content.replace(
    '.t-cb{width:20px;height:20px;border-radius:6px;border:2px solid var(--text-muted);background:var(--surface-2);display:flex;align-items:center;justify-content:center;flex-shrink:0;cursor:pointer;transition:all 0.2s;margin-left:12px;box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);}',
    '.t-cb{width:20px;height:20px;border-radius:6px;border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;flex-shrink:0;cursor:pointer;transition:all 0.2s;margin-left:12px;box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);}'
)

# Fix mastery glass fixed position
content = content.replace(
    '.mastery-glass { margin-top:2.5rem; background:var(--surface-1); padding:1.25rem; border-radius:12px; border:1px solid var(--border); box-shadow: 0 4px 15px rgba(0,0,0,0.1); position:relative; overflow:hidden; }',
    '.mastery-glass { position:fixed; bottom:0; left:0; right:0; z-index:100; margin:0; background:rgba(24,24,27,0.85); padding:1rem 2rem; border-top:1px solid var(--border); backdrop-filter:blur(24px); box-shadow: 0 -4px 15px rgba(0,0,0,0.2); }'
)

# And add padding to the bottom of the body so it doesn't get covered by the glass footer
content = content.replace(
    '</style>',
    'body { padding-bottom: 100px; }\n</style>',
    1
)

with open(file_path, 'w') as f:
    f.write(content)
print("Tracker patched.")
