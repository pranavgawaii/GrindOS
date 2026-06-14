import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

if "_mermaid_runtime" not in content:
    content = content.replace("from handbook_engine import _mermaid", "from handbook_engine import _mermaid, _mermaid_runtime")

if "{_mermaid_runtime()}" not in content:
    content = content.replace("</body>", "  {_mermaid_runtime()}\n</body>")

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Patched Mermaid runtime.")
