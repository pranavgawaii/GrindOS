import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

# Add imports for b_diagram and b_dossier if not there
if "from handbook_engine import b_diagram, b_dossier" not in content:
    content = content.replace("from handbook_engine import _mermaid, _mermaid_runtime", "from handbook_engine import _mermaid, _mermaid_runtime, b_diagram, b_dossier")

old_loop = content[content.find("# CONSTRUCT 80 CONTENT PAGES"):content.find("# COVER PAGE (PAGE 1)")]

new_loop = """# CONSTRUCT 80 CONTENT PAGES (3 pages per topic)
for t in topics_data:
    # ── PAGE 1: OVERVIEW & GRIDS ──
    page_1 = f'''
<div class="page" id="{t['id']}-p1">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="badge-yield">🔥 HIGH YIELD</div>
      <div class="header-badge">{t['section'].upper()}</div>
    </div>
  </div>
  
  <div class="topic-bar">
    <div class="topic-bar-top">
      <div class="topic-eyebrow">Topic {t['num']} &mdash; {t['section']}</div>
      <div class="yield-rating">Yield: <span class="stars-gold">★★★★★</span></div>
    </div>
    <div class="topic-title">{t['title']}</div>
  </div>
  
  <div class="body-container-sysdesign" style="flex:1; display:flex; flex-direction:column; gap:20px;">
    
    <div class="sysdesign-top-grid">
      <div class="sysdesign-card">
        <div class="sysdesign-card-title">📖 Definition &amp; Why It Exists</div>
        <p><strong>Definition:</strong> {t['def']}</p>
        <p style="margin-top: 4px;"><strong>Why It Exists:</strong> {t['why']}</p>
      </div>
      <div class="sysdesign-card">
        <div class="sysdesign-card-title">🌐 Real World Usage &amp; Tradeoff</div>
        <p><strong>Usage:</strong> {t['usage']}</p>
        <p style="margin-top: 4px;"><strong>Trade-off:</strong> {t['tradeoff']}</p>
      </div>
    </div>
    
    <div style="flex:1;"></div>

    <div class="sysdesign-bottom-placement-grid" style="min-height: 250px;">
      <div class="sysdesign-placement-block block-mistake">
        <div class="sysdesign-placement-block-title">⚠️ Common Mistake</div>
        <div>{t['mistake']}</div>
      </div>
      <div class="sysdesign-placement-block block-trap">
        <div class="sysdesign-placement-block-title">🛑 Interviewer Trap</div>
        <div>{t['questions']}</div>
      </div>
      <div class="sysdesign-placement-block block-followups">
        <div class="sysdesign-placement-block-title">🔄 Top Follow-Up</div>
        <div>{t['followups']}</div>
      </div>
      <div class="sysdesign-placement-block block-trick">
        <div class="sysdesign-placement-block-title">💡 Memory Trick</div>
        <div>{t['trick']}</div>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']}</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
    content_pages_html += page_1
    current_page_idx += 1

    # ── PAGE 2: ARCHITECTURE DOSSIER ──
    arch_diag = t.get('diagram_arch_data', {})
    if arch_diag:
        page_2 = f'''
<div class="page" id="{t['id']}-p2">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">ARCHITECTURE SPEC</div>
    </div>
  </div>
  
  <div style="padding: 16px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #FAF8F5;">
    {b_diagram(arch_diag)}
    {b_dossier(arch_diag)}
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']} (Architecture)</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
        content_pages_html += page_2
        current_page_idx += 1

    # ── PAGE 3: REQUEST FLOW DOSSIER ──
    flow_diag = t.get('diagram_flow_data', {})
    if flow_diag:
        page_3 = f'''
<div class="page" id="{t['id']}-p3">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">REQUEST FLOW SPEC</div>
    </div>
  </div>
  
  <div style="padding: 16px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #FAF8F5;">
    {b_diagram(flow_diag)}
    {b_dossier(flow_diag)}
    <div style="margin-top: 12px; padding: 12px; background: #fff; border: 1px solid #EBE5DB; border-radius: 4px; font-size: 8.5pt; color: #2D3748;">
      <p style="margin-bottom: 6px;"><strong>Request Flow:</strong> {t['flow']}</p>
      <p style="margin-bottom: 6px; color: #2F855A;"><strong>Pros:</strong> {t['pros']}</p>
      <p style="color: #C53030;"><strong>Cons:</strong> {t['cons']}</p>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']} (Request Flow)</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
        content_pages_html += page_3
        current_page_idx += 1

"""

content = content.replace(old_loop, new_loop)
content = content.replace("total_pages_count = 85", "total_pages_count = 240")

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Patched loop.")
