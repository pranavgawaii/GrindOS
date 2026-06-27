import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# The new Notion-style Notebook wrapper CSS and structure
NOTEBOOK_CSS = """
<style>
/* === Notion-Style Notebook Redesign === */
.nb-master-container {
    display: flex;
    height: 780px;
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    background: var(--surface-1);
    box-shadow: 0 8px 40px rgba(0,0,0,0.15);
    margin-top: 2rem;
}
.nb-sidebar {
    width: 260px;
    flex-shrink: 0;
    background: var(--surface-2);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
}
.nb-sidebar-head {
    padding: 1.5rem 1.25rem 1rem;
    border-bottom: 1px solid var(--border);
}
.nb-sidebar-head h3 {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-1);
    margin: 0 0 4px;
}
.nb-sidebar-head small {
    font-size: 0.78rem;
    color: var(--text-muted);
}
.nb-tabs-v {
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow-y: auto;
    flex: 1;
}
.nb-tab {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.92rem;
    font-weight: 500;
    color: var(--text-2);
    transition: all 0.15s;
    text-align: left;
    border: none;
    background: none;
    width: 100%;
}
.nb-tab:hover { background: var(--surface-0); color: var(--text-1); }
.nb-tab.active { background: rgba(255,94,0,0.1); color: var(--brand); font-weight: 600; }
.nb-tab-icon { width: 20px; height: 20px; flex-shrink: 0; opacity: 0.6; }
.nb-tab.active .nb-tab-icon { opacity: 1; }

.nb-content-pane {
    flex: 1;
    overflow-y: auto;
    background: var(--bg);
}
.nb-page {
    display: none;
    padding: 3.5rem 4rem;
    max-width: 720px;
}
.nb-page.active {
    display: block;
    animation: nbFadeIn 0.25s ease;
}
@keyframes nbFadeIn { from { opacity:0; transform: translateY(8px); } to { opacity:1; transform: none; } }

/* Typography inside notes */
.page-frame { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
.page-top {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.page-subject {
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--brand) !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
}
.page-dot { display: none !important; }
.page-title {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--text-1) !important;
    letter-spacing: -0.04em !important;
    line-height: 1.2 !important;
    margin: 0 0 6px !important;
}
.page-date {
    font-size: 0.85rem !important;
    color: var(--text-3) !important;
}
.ruled {
    background: transparent !important;
    background-image: none !important;
    padding: 0 !important;
}
.line {
    border-bottom: none !important;
    padding: 2px 0 !important;
    margin-bottom: 2px !important;
}
.line.blank { margin-bottom: 12px !important; }
.line-num { display: none !important; }
.line-content {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.75 !important;
    color: var(--text-2) !important;
    display: block !important;
}
.hl-purple, .hl-blue, .hl-coral, .hl-teal {
    display: block !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
    margin-top: 2rem !important;
    margin-bottom: 0.5rem !important;
    padding-bottom: 6px !important;
    border-bottom: 1px solid var(--border) !important;
}
.arrow {
    color: var(--brand) !important;
    font-weight: bold !important;
    margin-right: 10px !important;
    font-size: 1rem !important;
}
.indent {
    padding-left: 1.5rem !important;
    position: relative !important;
}
.sticky {
    background: rgba(255,94,0,0.05) !important;
    border-left: 3px solid var(--brand) !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 1.25rem 1.5rem !important;
    margin-top: 2.5rem !important;
    box-shadow: none !important;
    transform: none !important;
}
.sticky-title {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--brand) !important;
    margin-bottom: 6px !important;
}
.sticky p { color: var(--text-2) !important; font-size: 0.95rem !important; line-height: 1.6 !important; }
.warn-box {
    background: rgba(255,60,60,0.08) !important;
    border: 1px solid rgba(255,60,60,0.2) !important;
    border-radius: 8px !important;
    padding: 1.25rem !important;
    margin-top: 2rem !important;
    color: var(--text-1) !important;
}
</style>
"""

def rebuild_notebook(html):
    # 1. Remove old header for Interview Notes
    html = re.sub(
        r'<div class="dashboard-header-row"[^>]*>.*?<h2>Interview Notes Notebook</h2>.*?</div>\s*</div>',
        '',
        html,
        flags=re.DOTALL
    )
    
    # 2. Find the outer glass-card wrapper that contains the notebook
    # Pattern: <div class="glass-card stat-card" ... > \n <div class="nb-wrap">
    # We'll keep all the internal page content but wrap it in the new Notion-style container
    
    # Find start of glass-card containing nb-wrap
    glass_start = html.find('<div class="glass-card stat-card" style="padding: 2rem; margin-top: 2rem; border-top: 4px solid var(--brand); overflow-x: auto;">')
    if glass_start == -1:
        print("Could not find glass-card, trying alternate match...")
        glass_start = html.find('<div class="nb-wrap">')
        if glass_start == -1:
            print("Could not find nb-wrap either. Aborting notebook redesign.")
            return html
        wrap_start = glass_start
    else:
        wrap_start = html.find('<div class="nb-wrap">', glass_start)
    
    # Find end of the nb-wrap. It ends with </div> after the last nb-page
    # The notebook section ends right before the closing </div> of glass-card
    # Let's find the script tag after all nb-pages to determine end
    pages_end = html.find('\n    </div>\n    </div>\n  </div>', wrap_start)
    if pages_end == -1:
        # Try another closing pattern
        pages_end = html.find('</div>\n</div>', wrap_start)
    
    if pages_end == -1:
        print("Couldn't find notebook end. Skipping notebook redesign.")
        return html
    
    # Extract the existing nb-tabs and nb-pages content
    old_nb_section = html[wrap_start:pages_end + 20]
    
    # Extract all nb-page divs
    pages = re.findall(r'<div id="tab-\w+" class="nb-page[^"]*">.*?(?=<div id="tab-|\Z)', old_nb_section, flags=re.DOTALL)
    
    # Parse what tabs exist (excluding oop, dsa tabs since we don't need them)
    keep_tabs = ['os', 'dbms', 'tips', 'playbook']
    tab_labels = {
        'os': ('OS — Deadlock', '📋'),
        'dbms': ('DBMS — SQL', '🗃️'),
        'tips': ('Tips + Tricks', '💡'),
        'playbook': ('Fresher Playbook', '📖'),
        'guide': ('Complete Guide', '🗺️'),
    }
    
    # Extract the actual page HTML for each tab
    page_htmls = {}
    for tab_id in keep_tabs:
        match = re.search(rf'<div id="tab-{tab_id}" class="nb-page[^"]*">(.*?)(?=<div id="tab-|\Z)', old_nb_section, flags=re.DOTALL)
        if match:
            page_htmls[tab_id] = match.group(1).strip()
    
    # Build new sidebar tabs
    sidebar_tabs = ""
    for i, tab_id in enumerate(keep_tabs):
        label, icon = tab_labels.get(tab_id, (tab_id, '📄'))
        active_cls = " active" if i == 0 else ""
        sidebar_tabs += f"""
            <div class="nb-tab{active_cls}" onclick="switchTab('{tab_id}')">
                <span style="font-size:1rem; flex-shrink:0">{icon}</span>
                {label}
            </div>"""
    
    # Build new pages
    pages_html = ""
    for i, tab_id in enumerate(keep_tabs):
        active_cls = " active" if i == 0 else ""
        content = page_htmls.get(tab_id, '<p>No content.</p>')
        pages_html += f'<div id="tab-{tab_id}" class="nb-page{active_cls}">{content}</div>\n'
    
    new_notebook = f"""\n{NOTEBOOK_CSS}
<div class="nb-master-container">
    <div class="nb-sidebar">
        <div class="nb-sidebar-head">
            <h3>Interview Notes</h3>
            <small>Premium Workspace — Only what you need</small>
        </div>
        <div class="nb-tabs-v">
            {sidebar_tabs}
        </div>
    </div>
    <div class="nb-content-pane">
        {pages_html}
    </div>
</div>
"""
    
    # Now splice: replace from glass_start to pages_end+20
    replacement_end = html.find('</div>\n  </div>', pages_end)
    if replacement_end == -1:
        replacement_end = pages_end + 20
    else:
        replacement_end += len('</div>\n  </div>')
    
    html = html[:glass_start] + new_notebook + html[replacement_end:]
    
    return html


def remove_save_button(html):
    # Remove old fp-save-btn button HTML (not just CSS)
    html = re.sub(r'<button class="fp-save-btn"[^>]*>.*?</button>', '', html, flags=re.DOTALL)
    return html


for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if not os.path.exists(path):
        continue
    with open(path, "r") as f:
        html = f.read()
    
    html = rebuild_notebook(html)
    html = remove_save_button(html)
    
    with open(path, "w") as f:
        f.write(html)
    print(f"Done: {filename}")

print("Notebook rebuilt in Notion-style. Save Progress button removed.")
