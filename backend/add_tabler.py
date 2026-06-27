import os

filepath = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/tracker.html"
with open(filepath, 'r') as f:
    content = f.read()

# Add Tabler Icons to head
if 'tabler-icons' not in content:
    content = content.replace('</title>', '</title>\n  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">')

with open(filepath, 'w') as f:
    f.write(content)
