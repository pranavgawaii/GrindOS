import os
import re
from urllib.parse import urlparse, unquote

def check_links():
    base_dir = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend"
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files to check.")
    broken_count = 0

    # Match href="..." and src="..."
    link_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

    for html_path in html_files:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        links = link_pattern.findall(content)
        relative_dir = os.path.dirname(html_path)

        for link in links:
            # Clean url query/fragment
            parsed = urlparse(link)
            if parsed.scheme in ('http', 'https', 'mailto', 'tel', 'javascript'):
                continue
            if not parsed.path and parsed.fragment:
                # anchor link
                continue
            
            # Decode URL-encoded characters (like %20)
            path_part = unquote(parsed.path)
            if not path_part:
                continue

            # Resolve path relative to the file
            if path_part.startswith('/'):
                # Treat absolute path relative to frontend/
                target_path = os.path.join(base_dir, path_part.lstrip('/'))
            else:
                target_path = os.path.join(relative_dir, path_part)

            # Check if target exists
            if not os.path.exists(target_path):
                # Check with index.html if it is a directory link
                if not os.path.isdir(target_path) and os.path.exists(os.path.join(target_path, 'index.html')):
                    continue
                print(f"Broken link in {os.path.relpath(html_path, base_dir)}: {link} -> {os.path.relpath(target_path, base_dir)}")
                broken_count += 1

    print(f"Total broken links: {broken_count}")

if __name__ == '__main__':
    check_links()
