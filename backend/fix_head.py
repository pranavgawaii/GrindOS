import os

filepath = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/interview_qa.html"
with open(filepath, 'r') as f:
    content = f.read()

# Make sure we have the theme script in head
if "localStorage.getItem('GrindOS-theme')" not in content:
    theme_script = """
    <script>
      (function() {
        const saved = localStorage.getItem('GrindOS-theme');
        if (saved) {
          document.documentElement.classList.add(saved);
        } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
          document.documentElement.classList.add('dark');
        }
      })();
    </script>
    """
    content = content.replace('<title>', theme_script + '<title>')

# Also add favicon if missing
if 'href="/logo.png"' not in content:
    content = content.replace('<link rel="stylesheet" href="assets/style.css">', '<link rel="stylesheet" href="assets/style.css">\n    <link rel="icon" type="image/png" href="/logo.png">')

with open(filepath, 'w') as f:
    f.write(content)
