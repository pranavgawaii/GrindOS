import os
import re

frontend_dir = "frontend"

for root, _, files in os.walk(frontend_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            
            original_content = content
            
            # 1. Remove company-nav from topbar and mobile nav
            # Regex to match the whole line containing company-prep.html
            content = re.sub(r'^[ \t]*<a href="[^"]*company-prep\.html.*</a>\n?', '', content, flags=re.MULTILINE)
            
            # 2. Add resume-nav if missing
            if 'class="topbar-nav"' in content and 'class="resume-nav"' not in content:
                # Find prep-nav line to know the relative path depth
                match = re.search(r'^[ \t]*<a href="([^"]*)interview-prep/index\.html"[^>]*>Prep</a>\n?', content, flags=re.MULTILINE)
                if match:
                    relative_prefix = match.group(1)
                    resume_line = f'    <a href="{relative_prefix}resume-builder.html" class="resume-nav">Resume</a>\n'
                    # Insert after prep-nav
                    content = content.replace(match.group(0), match.group(0) + resume_line)
                    
            if content != original_content:
                with open(path, "w") as f:
                    f.write(content)
                print(f"Updated {path}")
