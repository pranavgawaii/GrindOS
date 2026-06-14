import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

# Add import
if "from handbook_engine import _mermaid" not in content:
    content = content.replace("import os", "import os\nfrom handbook_engine import _mermaid")

# Add CD string
cd_string = """
CD = '''classDef client fill:#FBF8F4,stroke:#EA763F,stroke-width:2px,color:#0F172A;
classDef svc fill:#EFF4FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
classDef data fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#0F172A;
classDef queue fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#0F172A;
classDef ext fill:#F5F3FF,stroke:#7C3AED,stroke-width:2px,color:#0F172A;
classDef bad fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#0F172A;
'''
"""
if "CD =" not in content:
    content = content.replace("topics_data = [", cd_string + "\ntopics_data = [")

# Replace mid grid
old_mid_grid = """    <div class="sysdesign-mid-grid">
      <div class="sysdesign-diagram-box">
        <div class="sysdesign-card-title" style="margin-bottom: 2px;">⚡ Architecture Diagram</div>
        <pre class="sysdesign-ascii-diag">{t['diagram'].strip()}</pre>
      </div>
      <div class="sysdesign-flow-box">
        <div class="sysdesign-card-title">🔄 Request Flow &amp; Tradeoffs</div>
        <p><strong>Flow:</strong> {t['flow']}</p>
        <p style="margin-top: 4px;"><strong>Pros:</strong> {t['pros']}</p>
        <p><strong>Cons:</strong> {t['cons']}</p>
      </div>
    </div>"""

new_mid_grid = """    <div class="sysdesign-mid-grid">
      <div class="sysdesign-diagram-box" style="background:#fff; color:#111; padding:0; border: 1px solid #CBD5E0;">
        <div class="sysdesign-card-title" style="padding: 8px 8px 0 8px; color: #EA763F;">⚡ Architecture Diagram</div>
        {_mermaid(CD + t['diagram'], t['id']+"-arch") if 'flowchart' in t['diagram'] or 'sequenceDiagram' in t['diagram'] else f'<pre class="sysdesign-ascii-diag" style="color:#F7FAFC; background:#2D3748; margin:0; padding:8px; height:100%;">{t["diagram"].strip()}</pre>'}
      </div>
      <div class="sysdesign-flow-box" style="display:flex; flex-direction:column; padding:0; background:#fff; overflow:hidden;">
        <div class="sysdesign-card-title" style="padding: 8px 8px 0 8px; color: #EA763F;">🔄 Request Flow</div>
        <div style="flex:1; min-height:0; display:flex; flex-direction:column;">
          {_mermaid(t['flow_diagram'], t['id']+"-flow") if 'flow_diagram' in t else ''}
        </div>
        <div style="padding: 8px; border-top: 1px solid #EBE5DB; background: #FCFAF7;">
            <p><strong>Flow:</strong> {t['flow']}</p>
            <p style="margin-top: 4px;"><strong>Pros:</strong> {t['pros']}</p>
            <p><strong>Cons:</strong> {t['cons']}</p>
        </div>
      </div>
    </div>"""

content = content.replace(old_mid_grid, new_mid_grid)

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Patched rendering template.")
