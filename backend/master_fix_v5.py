import os
import re
from datetime import datetime, timedelta

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")
START_DATE = datetime(2026, 6, 26)

# ── STEP 1: Re-parse all data for audit report ─────────────────────────────
notebook_path = os.path.join(ROOT, "interview_notes_notebook.html")
with open(notebook_path, "r") as f:
    nb_content = f.read()

guide_section = nb_content.split('id="tab-guide"')[1].split('id="tab-playbook"')[0]
nb_lines = re.findall(r'<span class="line-content">(.*?)</span>', guide_section)

blocks_data = []
current_block = None

for line in nb_lines:
    text = re.sub(r'<[^>]+>', '', line).strip()
    block_match = re.search(r'###\s*(BLOCK\s+(\d+)\s*[—\-]\s*[^\(]+)', text)
    if block_match:
        block_title = block_match.group(1).strip()
        clean_title = re.sub(r'BLOCK\s+\d+\s*[—\-]\s*', '', block_title).strip()
        block_num = int(block_match.group(2))
        current_block = {"num": block_num, "title": clean_title, "items": [], "days": 0}
        blocks_data.append(current_block)
        continue
    if current_block:
        topic_match = re.match(r'^(\d+)\.\s+(.*)', text)
        if topic_match:
            current_block["items"].append({"type": "topic", "id": topic_match.group(1), "text": topic_match.group(2)})
        else:
            sub_match = re.match(r'^-\s+(.*)', text)
            if sub_match and current_block["items"]:
                current_block["items"].append({"type": "subtopic", "id": f"{current_block['items'][-1]['id']}_s{len(current_block['items'])}", "text": sub_match.group(1)})

roadmap_path = "/Users/8teen/Downloads/fresher_placement_roadmap.html"
with open(roadmap_path, "r") as f:
    rm_content = f.read()

rm_blocks = rm_content.split('<div class="block">')[1:]
block_meta = {}  # num -> {days, resources, notes, tips}
for rm_block in rm_blocks:
    num_match = re.search(r'<div class="block-num">Block (\d+)', rm_block)
    if not num_match: continue
    b_num = int(num_match.group(1))
    meta = {"days": 0, "resources": "", "notes": "", "tips": ""}
    dur_match = re.search(r'>(\d+)\s*days<', rm_block)
    if dur_match: meta["days"] = int(dur_match.group(1))
    res_match = re.search(r'<div class="res-row">(.*?)</div>\s*<div', rm_block, flags=re.DOTALL)
    if not res_match: res_match = re.search(r'<div class="res-row">(.*?)</div>', rm_block, flags=re.DOTALL)
    if res_match: meta["resources"] = res_match.group(1).strip()
    notes_match = re.search(r'<div class="note-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if notes_match: meta["notes"] = notes_match.group(1).strip()
    tips_match = re.search(r'<div class="tip-box">(.*?)</div>', rm_block, flags=re.DOTALL)
    if tips_match: meta["tips"] = tips_match.group(1).strip()
    block_meta[b_num] = meta

for block in blocks_data:
    meta = block_meta.get(block["num"], {})
    block["days"] = meta.get("days", 0)
    block["resources"] = meta.get("resources", "")
    block["notes"] = meta.get("notes", "")
    block["tips"] = meta.get("tips", "")

# Calculate dates
current_date = START_DATE
total_topics = 0
for block in blocks_data:
    block["start_date"] = current_date
    block["end_date"] = current_date + timedelta(days=block["days"])
    num_items = len(block["items"])
    if num_items > 0:
        days_per = block["days"] / num_items
        for i, item in enumerate(block["items"]):
            item["due_date"] = current_date + timedelta(days=(i + 1) * days_per)
        total_topics += num_items
    current_date = block["end_date"]

# ── STEP 2: Generate Audit Report text ────────────────────────────────────
report_lines = ["=" * 70]
report_lines.append("ROADMAP TRACKER — FULL AUDIT REPORT")
report_lines.append(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
report_lines.append(f"Start Date: Jun 26, 2026")
report_lines.append(f"Total Topics: {total_topics}")
report_lines.append("=" * 70)

for block in blocks_data:
    if not block["items"]: continue
    report_lines.append("")
    report_lines.append(f"╔ {block['title'].upper()}")
    report_lines.append(f"  Target: {block['start_date'].strftime('%b %d, %Y')} → {block['end_date'].strftime('%b %d, %Y')}  ({block['days']} days)")
    report_lines.append("")
    for item in block["items"]:
        due = item["due_date"].strftime("%b %d, %Y")
        if item["type"] == "topic":
            report_lines.append(f"  [{item['id']}] {item['text']}")
            report_lines.append(f"       Due: {due}")
        else:
            report_lines.append(f"       └─ {item['text']}")
            report_lines.append(f"          Due: {due}")

report_lines.append("")
report_lines.append("=" * 70)
report_lines.append("END OF REPORT")
report_text = "\n".join(report_lines)

report_path = os.path.join(ROOT, "TRACKER_AUDIT_REPORT.txt")
with open(report_path, "w") as f:
    f.write(report_text)
print(f"✓ Audit report saved: {report_path}")
print()
print(report_text[:3000])

# ── STEP 3: Build new TRACKER HTML ────────────────────────────────────────
tracker_css = """<style>
/* ─── Metrics Matrix ─── */
.metrics-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 2.5rem; }
.metric-box { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem 1rem; display:flex; flex-direction:column; gap:4px; position:relative; overflow:hidden; }
.metric-box::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; background: var(--border-strong); }
.overdue-box::after { background: #ff4757; }
.metric-val { font-size:2rem; font-weight:800; color:var(--text-1); line-height:1; }
.metric-lbl { font-size:0.75rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); font-weight:600; }
.overdue-val { color:#ff4757 !important; }

/* ─── Checklist Container ─── */
.checklist-master-container { max-width:900px; margin:0 auto; padding:0 1rem 140px; }
.tracker-hero { margin-bottom:2rem; }
.tracker-hero h1 { font-size:1.8rem; font-weight:800; color:var(--text-1); }
.tracker-hero p { font-size:0.95rem; color:var(--text-3); margin-top:4px; }

/* ─── Accordion Cards ─── */
.acc-card { background:var(--surface-1); border:1px solid var(--border); border-radius:12px; margin-bottom:1rem; overflow:hidden; transition:border-color .2s; }
.acc-card:hover { border-color:var(--border-strong); }
.acc-header { padding:1rem 1.25rem; background:var(--surface-2); display:flex; align-items:center; justify-content:space-between; cursor:pointer; user-select:none; }
.acc-header-left { display:flex; flex-direction:column; align-items:flex-start; gap:5px; }
.acc-title { font-size:0.95rem; font-weight:700; color:var(--text-1); text-transform:uppercase; letter-spacing:0.04em; text-align:left; }
.acc-date-range { display:inline-flex; align-items:center; gap:5px; font-size:0.78rem; color:var(--text-3); font-weight:500; }
.acc-date-range svg { opacity:0.5; }
.acc-chevron { flex-shrink:0; color:var(--text-3); transition:transform .25s; }
.acc-card.open .acc-chevron { transform:rotate(180deg); }
.acc-body { display:none; border-top:1px solid var(--border); }
.acc-card.open .acc-body { display:block; }

/* ─── Task List ─── */
.task-list { padding:0.75rem 1rem; display:flex; flex-direction:column; gap:2px; }
.task-item { display:flex; align-items:flex-start; gap:10px; padding:8px 10px; border-radius:7px; cursor:pointer; transition:background .15s; width:100%; text-align:left; }
.task-item:hover { background:var(--surface-0); }
.task-item.subtopic { margin-left:1.75rem; position:relative; }
.task-item.subtopic::before { content:''; position:absolute; left:-12px; top:0; bottom:50%; width:1px; background:var(--border); }
.task-item.subtopic::after { content:''; position:absolute; left:-12px; top:50%; width:12px; height:1px; background:var(--border); }
.task-checkbox { display:none; }
.task-box { width:18px; height:18px; border-radius:4px; border:2px solid var(--text-4); display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:2px; transition:all .15s; }
.task-checkbox:checked + .task-box { background:var(--text-1); border-color:var(--text-1); }
.task-checkbox:checked + .task-box::after { content:'✓'; color:var(--bg); font-size:12px; font-weight:800; line-height:1; }
.task-body { flex:1; display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; min-width:0; }
.task-label { font-size:0.9rem; color:var(--text-1); line-height:1.5; text-align:left; }
.task-num { color:var(--brand); font-weight:700; margin-right:5px; }
.task-checkbox:checked ~ .task-body .task-label { color:var(--text-4); text-decoration:line-through; }
.task-due-badge { font-size:0.72rem; font-weight:600; padding:2px 7px; border-radius:10px; white-space:nowrap; flex-shrink:0; margin-top:3px; }
.due-normal { color:var(--text-muted); background:var(--surface-0); border:1px solid var(--border); }
.due-overdue { color:#ff4757; background:rgba(255,71,87,.1); border:1px solid rgba(255,71,87,.25); }
.task-checkbox:checked ~ .task-body .task-due-badge { opacity:.4; text-decoration:line-through; }

/* ─── Block Meta ─── */
.block-meta { padding:1rem 1.25rem 1.25rem; border-top:1px solid var(--border); display:flex; flex-direction:column; gap:1rem; }
.meta-label { font-size:0.75rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-muted); font-weight:600; margin-bottom:6px; }
.info-note { padding:.85rem 1rem; border-radius:8px; font-size:.88rem; line-height:1.6; }
.info-note.warn { background:rgba(245,166,35,.08); border:1px solid rgba(245,166,35,.2); color:var(--text-1); }
.info-note.warn b { color:#f5a623; }
.info-note.tip  { background:rgba(46,213,115,.08); border:1px solid rgba(46,213,115,.2);  color:var(--text-1); }
.info-note.tip  b { color:#2ed573; }
.res-list { display:flex; flex-direction:column; gap:6px; }
.res-link { display:flex; align-items:center; gap:8px; padding:9px 12px; background:var(--surface-0); border:1px solid var(--border); border-radius:7px; color:var(--text-1); text-decoration:none; font-size:.88rem; transition:border-color .15s; }
.res-link:hover { border-color:var(--text-3); }

/* ─── Floating pill ─── */
.fp-pill { position:fixed; bottom:1.5rem; left:50%; transform:translateX(-50%); background:var(--surface-2); border:1px solid var(--border-strong); border-radius:100px; padding:12px 28px; display:flex; align-items:center; gap:20px; width:90%; max-width:480px; box-shadow:0 8px 30px rgba(0,0,0,.35); z-index:1000; backdrop-filter:blur(12px); }
.fp-info { flex:1; }
.fp-row { display:flex; justify-content:space-between; font-size:.82rem; font-weight:600; color:var(--text-2); margin-bottom:6px; }
.fp-track { height:6px; background:var(--surface-0); border-radius:3px; overflow:hidden; }
.fp-fill { height:100%; background:var(--text-1); border-radius:3px; width:0%; transition:width .3s; }
</style>"""

blocks_html = ""
for block in blocks_data:
    if not block["items"]: continue

    items_html = ""
    for item in block["items"]:
        is_sub = item["type"] == "subtopic"
        cls = "task-item subtopic" if is_sub else "task-item"
        prefix = f"<span class='task-num'>{item['id']}.</span>" if not is_sub else ""
        due_iso = item["due_date"].strftime("%Y-%m-%d")
        due_disp = item["due_date"].strftime("%b %d")
        items_html += f"""
        <label class="{cls}">
          <input type="checkbox" class="task-checkbox" id="t-{item['id']}" data-due="{due_iso}">
          <div class="task-box"></div>
          <div class="task-body">
            <span class="task-label">{prefix}{item['text']}</span>
            <span class="task-due-badge due-normal" id="badge-{item['id']}">{due_disp}</span>
          </div>
        </label>"""

    meta_html = ""
    parts = []
    if block["resources"]:
        parts.append(f"<div><div class='meta-label'>Resources</div><div class='res-list'>{block['resources']}</div></div>")
    if block["notes"]:
        parts.append(f"<div><div class='meta-label'>Notes Strategy</div><div class='info-note warn'>{block['notes']}</div></div>")
    if block["tips"]:
        parts.append(f"<div><div class='meta-label'>Tips</div><div class='info-note tip'>{block['tips']}</div></div>")
    if parts:
        meta_html = f"<div class='block-meta'>{''.join(parts)}</div>"

    start_s = block["start_date"].strftime("%b %d")
    end_s = block["end_date"].strftime("%b %d, %Y")

    blocks_html += f"""
    <div class="acc-card" onclick="toggleAcc(this)">
      <div class="acc-header">
        <div class="acc-header-left">
          <span class="acc-title">{block['title']}</span>
          <span class="acc-date-range">
            <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            {start_s} → {end_s} · {block['days']} days
          </span>
        </div>
        <div class="acc-chevron">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>
      <div class="acc-body">
        <div class="task-list">{items_html}</div>
        {meta_html}
      </div>
    </div>"""

new_tracker = f"""{tracker_css}
<div class="checklist-master-container" id="checklist-master">
  <div class="tracker-hero">
    <h1>Roadmap Tracker</h1>
    <p>Live deadlines calculated from Jun 26, 2026. Check off as you go.</p>
  </div>
  <div class="metrics-grid">
    <div class="metric-box">
      <span class="metric-val" id="m-total">{total_topics}</span>
      <span class="metric-lbl">Total</span>
    </div>
    <div class="metric-box">
      <span class="metric-val" id="m-done">0</span>
      <span class="metric-lbl">Completed</span>
    </div>
    <div class="metric-box">
      <span class="metric-val" id="m-left">{total_topics}</span>
      <span class="metric-lbl">Remaining</span>
    </div>
    <div class="metric-box overdue-box">
      <span class="metric-val overdue-val" id="m-overdue">0</span>
      <span class="metric-lbl">Overdue</span>
    </div>
  </div>
  <div>{blocks_html}</div>
</div>
<div class="fp-pill">
  <div class="fp-info">
    <div class="fp-row"><span>Overall Mastery</span><span id="fp-pct">0%</span></div>
    <div class="fp-track"><div class="fp-fill" id="fp-bar"></div></div>
  </div>
</div>
<script>
function toggleAcc(el) {{
  el.classList.toggle('open');
}}
function syncProgress() {{
  const all = document.querySelectorAll('.task-checkbox');
  const today = new Date(); today.setHours(0,0,0,0);
  let done = 0, overdue = 0;
  all.forEach(cb => {{
    const checked = cb.checked;
    if (checked) done++;
    const due = cb.getAttribute('data-due');
    const badgeId = 'badge-' + cb.id.split('-')[1];
    const badge = document.getElementById(badgeId);
    if (badge && due) {{
      const d = new Date(due);
      if (!checked && d < today) {{
        overdue++;
        badge.className = 'task-due-badge due-overdue';
        badge.textContent = 'Overdue';
      }} else if (!badge.classList.contains('due-overdue') || checked) {{
        badge.className = 'task-due-badge due-normal';
        badge.textContent = d.toLocaleDateString('en-US', {{month:'short', day:'numeric'}});
      }}
    }}
  }});
  document.getElementById('m-done').textContent = done;
  document.getElementById('m-left').textContent = all.length - done;
  document.getElementById('m-overdue').textContent = overdue;
  const pct = all.length ? Math.round(done/all.length*100) : 0;
  document.getElementById('fp-pct').textContent = pct + '%';
  document.getElementById('fp-bar').style.width = pct + '%';
}}
document.querySelectorAll('.task-checkbox').forEach(cb => {{
  const saved = localStorage.getItem('go-' + cb.id);
  if (saved === '1') cb.checked = true;
  cb.addEventListener('change', e => {{
    localStorage.setItem('go-' + cb.id, e.target.checked ? '1' : '0');
    syncProgress();
  }});
}});
window.addEventListener('DOMContentLoaded', syncProgress);
</script>"""

# ── STEP 4: Rebuild Notebook content pane with REAL content ───────────────
# Read the source — the real content is in interview_notes_notebook.html
with open(notebook_path, "r") as f:
    nb_src = f.read()

def extract_page(src, tab_id):
    """Extract inner content of <div id='tab-{tab_id}' ...>...</div>"""
    # Find the div
    pat = rf'<div id="tab-{tab_id}" class="nb-page[^"]*">(.*?)(?=<div id="tab-|\Z)'
    m = re.search(pat, src, flags=re.DOTALL)
    if m:
        return m.group(1).strip()
    return "<p>Content not found.</p>"

keep_tabs = [
    ("os",       "OS — Deadlock",    "📋"),
    ("dbms",     "DBMS — SQL",       "🗃️"),
    ("tips",     "Tips + Tricks",    "💡"),
    ("playbook", "Fresher Playbook", "📖"),
]

sidebar_items = ""
pages_html = ""
for i, (tid, label, icon) in enumerate(keep_tabs):
    active = " active" if i == 0 else ""
    sidebar_items += f"""
            <div class="nb-tab{active}" onclick="switchTab('{tid}')">
              <span style="font-size:1.1rem">{icon}</span> {label}
            </div>"""
    content = extract_page(nb_src, tid)
    pages_html += f'<div id="tab-{tid}" class="nb-page{active}">{content}</div>\n'

notebook_css_str = """<style>
/* ─── Notion Notebook ─── */
.nb-master-container{display:flex;height:800px;border:1px solid var(--border);border-radius:14px;overflow:hidden;background:var(--surface-1);box-shadow:0 8px 40px rgba(0,0,0,.15);margin-top:1.5rem;}
.nb-sidebar{width:240px;flex-shrink:0;background:var(--surface-2);border-right:1px solid var(--border);display:flex;flex-direction:column;}
.nb-sidebar-head{padding:1.25rem 1rem 1rem;border-bottom:1px solid var(--border);}
.nb-sidebar-head h3{font-size:.95rem;font-weight:700;color:var(--text-1);margin:0 0 3px;}
.nb-sidebar-head small{font-size:.75rem;color:var(--text-muted);}
.nb-tabs-v{padding:.5rem;display:flex;flex-direction:column;gap:2px;overflow-y:auto;flex:1;}
.nb-tab{display:flex;align-items:center;gap:9px;padding:10px 10px;border-radius:7px;cursor:pointer;font-size:.88rem;font-weight:500;color:var(--text-2);transition:all .15s;text-align:left;border:none;background:none;width:100%;}
.nb-tab:hover{background:var(--surface-0);color:var(--text-1);}
.nb-tab.active{background:rgba(255,94,0,.1);color:var(--brand);font-weight:600;}
.nb-content-pane{flex:1;overflow-y:auto;background:var(--bg);}
.nb-page{display:none;padding:3rem 3.5rem;max-width:700px;}
.nb-page.active{display:block;animation:nbIn .2s ease;}
@keyframes nbIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* Typography overrides */
.page-frame{background:transparent!important;border:none!important;box-shadow:none!important;padding:0!important;}
.page-top{margin-bottom:2.5rem;padding-bottom:1.25rem;border-bottom:1px solid var(--border);}
.page-dot{display:none!important;}
.page-subject{font-size:.75rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;color:var(--brand)!important;font-weight:700!important;margin-bottom:6px!important;}
.page-title{font-size:2rem!important;font-weight:800!important;color:var(--text-1)!important;letter-spacing:-.03em!important;line-height:1.2!important;margin:0!important;}
.page-date{font-size:.82rem!important;color:var(--text-3)!important;margin-top:6px!important;}
.ruled{background:transparent!important;background-image:none!important;padding:0!important;}
.line{border-bottom:none!important;padding:1px 0!important;margin-bottom:1px!important;}
.line.blank{margin-bottom:10px!important;}
.line-num{display:none!important;}
.line-content{font-family:'Inter',sans-serif!important;font-size:.97rem!important;line-height:1.75!important;color:var(--text-2)!important;display:block!important;}
.hl-purple,.hl-blue,.hl-coral,.hl-teal{display:block!important;font-size:1.1rem!important;font-weight:700!important;color:var(--text-1)!important;margin-top:2rem!important;margin-bottom:.35rem!important;padding-bottom:5px!important;border-bottom:1px solid var(--border)!important;}
.arrow{color:var(--brand)!important;font-weight:bold!important;margin-right:8px!important;}
.indent{padding-left:1.25rem!important;}
.sticky{background:rgba(255,94,0,.05)!important;border-left:3px solid var(--brand)!important;border-top:none!important;border-right:none!important;border-bottom:none!important;border-radius:0 8px 8px 0!important;padding:1rem 1.25rem!important;margin-top:2rem!important;box-shadow:none!important;transform:none!important;}
.sticky-title{font-size:.82rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.05em!important;color:var(--brand)!important;margin-bottom:4px!important;}
.sticky p{color:var(--text-2)!important;font-size:.9rem!important;line-height:1.6!important;margin:0!important;}
.warn-box{background:rgba(255,60,60,.07)!important;border:1px solid rgba(255,60,60,.2)!important;border-radius:8px!important;padding:1rem!important;margin-top:1.5rem!important;color:var(--text-1)!important;font-size:.9rem!important;line-height:1.6!important;}
</style>"""

new_notebook = f"""{notebook_css_str}
<div class="nb-master-container">
  <div class="nb-sidebar">
    <div class="nb-sidebar-head">
      <h3>Interview Notes</h3>
      <small>Only what's needed to pass</small>
    </div>
    <div class="nb-tabs-v">
      {sidebar_items}
    </div>
  </div>
  <div class="nb-content-pane">
    {pages_html}
  </div>
</div>"""

# ── STEP 5: Apply to htmlfresher.html ─────────────────────────────────────
for filename in ["htmlfresher.html", "daily-checkin.html"]:
    path = os.path.join(FRONTEND, filename)
    if not os.path.exists(path):
        continue
    with open(path, "r") as f:
        html = f.read()

    # --- Replace Tracker ---
    t_start = html.find('<div class="checklist-master-container"')
    if t_start == -1:
        # Try old style CSS wrapper
        t_start = html.find('\n<style>\n/* Metrics Matrix */')
        if t_start == -1:
            t_start = html.find('\n<style>\n/* Live Tracking')
    if t_start != -1:
        t_end = html.find('</script>', t_start)
        if t_end != -1:
            t_end += len('</script>')
            html = html[:t_start] + new_tracker + html[t_end:]
            print(f"  ✓ Tracker replaced in {filename}")
        else:
            print(f"  ✗ Could not find tracker end in {filename}")
    else:
        print(f"  ✗ Could not find tracker start in {filename}")

    # --- Replace Notebook ---
    # Find the nb-master-container inserted last time (with "No content") and everything after until </div></div>
    nb_start = html.find('<div class="nb-master-container">')
    if nb_start != -1:
        # Find end of old nb-master-container (the closing </div> after all the duplicate orphan pages)
        # Look for the script switchTab which signals end of notebook section
        nb_end = html.find('<script>\nfunction switchTab', nb_start)
        if nb_end == -1:
            nb_end = html.find("function switchTab", nb_start)
        if nb_end != -1:
            end_script = html.find('</script>', nb_end) + len('</script>')
            html = html[:nb_start] + new_notebook + html[end_script:]
            print(f"  ✓ Notebook replaced in {filename}")
        else:
            # Find the closing of nb-master-container manually
            depth = 0
            idx = nb_start
            while idx < len(html):
                if html[idx:idx+4] == '<div':
                    depth += 1
                elif html[idx:idx+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        html = html[:nb_start] + new_notebook + html[idx+6:]
                        print(f"  ✓ Notebook replaced (depth) in {filename}")
                        break
                idx += 1
    else:
        # Find by glass-card wrapper
        glass = html.find('<div class="glass-card stat-card" style="padding: 2rem; margin-top: 2rem; border-top: 4px solid var(--brand); overflow-x: auto;">')
        if glass != -1:
            end_script = html.find('</script>', glass) + len('</script>')
            # Move past closing tags
            extra_closes = html[end_script:end_script+30]
            close_idx = end_script
            while html[close_idx:close_idx+6] in ('</div>', '\n</div', '    </'):
                close_idx = html.find('</div>', close_idx) + 6
                break
            html = html[:glass] + new_notebook + html[close_idx:]
            print(f"  ✓ Notebook replaced (glass) in {filename}")
        else:
            print(f"  ✗ Could not find notebook start in {filename}")

    with open(path, "w") as f:
        f.write(html)

print("\nAll done! Audit report, tracker, and notebook all updated.")
