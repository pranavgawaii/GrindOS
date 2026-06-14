with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

# I need to fix: \'code\': """
content = content.replace("\\'code\\':", '"code":')
content = content.replace("\\'eraser\\':", '"eraser":')

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Fixed backslashes.")
