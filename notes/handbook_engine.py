"""
GrindOS Premium Handbook — Shared Rendering Engine
==================================================
A block-based renderer that turns structured Python content into a
premium, ByteByteGo-grade A4 handbook with Mermaid vector diagrams.

Design language
---------------
  • A4 portrait pages, fixed grid, generous whitespace.
  • Navy ink (#0F172A) on warm white (#FFFFFF) with a single warm accent (#EA763F)
    plus a cool architecture-blue (#2563EB) for diagram flows.
  • Mermaid is themed (theme='base') so every diagram is on-brand — no purple defaults.
  • Playwright waits for networkidle, so Mermaid renders to real SVG before PDF capture.

Public API
----------
  render_book(meta, pages)  -> full HTML string
  Block helpers below build the `pages` list. Each page is a dict:
     {"kind": "...", ...fields}
  See PAGE KINDS at the bottom for the catalogue.
"""

import base64, os, html as _html

# ──────────────────────────────────────────────────────────────────────────────
# Asset loading
# ──────────────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
def _load_logo():
    for p in ["../logo.png", "../logo_cropped.png", "logo.png"]:
        fp = os.path.join(_HERE, p)
        if os.path.exists(fp):
            with open(fp, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""
LOGO_B64 = _load_logo()

def esc(s):
    return _html.escape(str(s), quote=False)

# ──────────────────────────────────────────────────────────────────────────────
# PALETTE  — single source of truth, mirrored into Mermaid themeVariables
# ──────────────────────────────────────────────────────────────────────────────
INK      = "#0F172A"   # near-black navy
INK_SOFT = "#334155"   # body text
MUTE     = "#64748B"   # secondary text
HAIR     = "#E2E8F0"   # hairline borders
PAPER    = "#FFFFFF"
CREAM    = "#FBF8F4"   # warm panel
ACCENT   = "#EA763F"   # GrindOS orange
ACCENT_D = "#C2410C"   # deep orange
BLUE     = "#2563EB"   # architecture blue
BLUE_BG  = "#EFF4FF"
GREEN    = "#059669"
GREEN_BG = "#ECFDF5"
RED      = "#DC2626"
RED_BG   = "#FEF2F2"
AMBER    = "#D97706"
AMBER_BG = "#FFFBEB"
VIOLET   = "#7C3AED"
VIOLET_BG= "#F5F3FF"

# ──────────────────────────────────────────────────────────────────────────────
# CSS  — the premium design system
# ──────────────────────────────────────────────────────────────────────────────
def _css():
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
@page {{ size: A4 portrait; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ font-family:'Inter',sans-serif; background:#D9DEE6; color:{INK_SOFT}; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}

.page {{
  width:210mm; height:297mm; background:{PAPER}; position:relative;
  display:flex; flex-direction:column; overflow:hidden;
  page-break-after:always; break-after:page;
  box-shadow:0 10px 40px rgba(15,23,42,.18); margin:14px auto;
}}
@media print {{ body{{background:#fff;}} .page{{margin:0; box-shadow:none;}} }}

/* ── running header / footer ── */
.rh {{ height:13mm; flex-shrink:0; display:flex; align-items:center; justify-content:space-between;
      padding:0 14mm; border-bottom:1px solid {HAIR}; }}
.rh-l {{ display:flex; align-items:center; gap:9px; }}
.rh-l img {{ height:17px; }}
.rh-wm {{ font-family:'Sora'; font-weight:800; font-size:11pt; color:{INK}; letter-spacing:-.3px; }}
.rh-wm span {{ color:{ACCENT}; }}
.rh-r {{ display:flex; align-items:center; gap:8px; }}
.chip {{ font-size:7pt; font-weight:700; letter-spacing:.4px; text-transform:uppercase;
        padding:3px 8px; border-radius:20px; }}
.chip-mute {{ color:{MUTE}; background:#F1F5F9; }}
.chip-acc  {{ color:{ACCENT_D}; background:{AMBER_BG}; border:1px solid #FCE6CF; }}
.chip-blue {{ color:{BLUE}; background:{BLUE_BG}; }}
.chip-green{{ color:{GREEN}; background:{GREEN_BG}; }}

.rf {{ position:absolute; bottom:0; left:0; right:0; height:11mm; display:flex;
      align-items:center; justify-content:space-between; padding:0 14mm;
      font-size:7.5pt; color:{MUTE}; border-top:1px solid {HAIR}; }}
.rf b {{ color:{INK}; font-weight:700; }}

/* ── section masthead (L2) ── */
.mast {{ padding:11px 14mm 9px; border-bottom:1px solid {HAIR}; flex-shrink:0;
        background:linear-gradient(180deg,{CREAM},#fff); }}
.mast-top {{ display:flex; align-items:center; justify-content:space-between; }}
.mast-eyebrow {{ font-family:'Sora'; font-size:8pt; font-weight:700; letter-spacing:1.5px;
                text-transform:uppercase; color:{ACCENT}; }}
.mast-yield {{ font-size:8pt; font-weight:600; color:{MUTE}; }}
.mast-yield b {{ color:{ACCENT_D}; }}
.mast-title {{ font-family:'Sora'; font-size:18pt; font-weight:800; color:{INK};
              letter-spacing:-.6px; line-height:1.05; margin-top:2px; }}
.mast-sub {{ font-size:8.5pt; color:{MUTE}; margin-top:2px; font-weight:500; }}
.mast-num {{ font-family:'Sora'; font-size:30pt; font-weight:800; color:{HAIR};
            line-height:.8; letter-spacing:-1px; }}

/* ── body ── */
.body {{ flex:1; overflow:hidden; padding:13px 14mm 15mm; display:flex; flex-direction:column; gap:11px; }}
.lead {{ font-size:9.5pt; line-height:1.5; color:{INK_SOFT}; }}
.lead b {{ color:{INK}; font-weight:700; }}

/* ── KPI / stat strip ── */
.kpis {{ display:grid; gap:9px; }}
.kpi {{ border:1px solid {HAIR}; border-radius:11px; padding:11px 13px; background:#fff;
       position:relative; overflow:hidden; }}
.kpi::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:{ACCENT}; }}
.kpi-v {{ font-family:'Sora'; font-size:18pt; font-weight:800; color:{INK}; letter-spacing:-.5px; line-height:1; }}
.kpi-l {{ font-size:7.5pt; font-weight:600; color:{MUTE}; text-transform:uppercase; letter-spacing:.5px; margin-top:5px; }}
.kpi.b::before{{background:{BLUE};}} .kpi.g::before{{background:{GREEN};}}
.kpi.r::before{{background:{RED};}}  .kpi.v::before{{background:{VIOLET};}}

/* ── feature / concept cards ── */
.cards {{ display:grid; gap:10px; }}
.card {{ border:1px solid {HAIR}; border-radius:12px; padding:12px 13px; background:#fff;
        display:flex; flex-direction:column; gap:5px; }}
.card-ic {{ font-size:15pt; line-height:1; }}
.card-h {{ font-family:'Sora'; font-size:9.5pt; font-weight:700; color:{INK}; }}
.card-p {{ font-size:8.3pt; line-height:1.5; color:{INK_SOFT}; }}
.card-p b {{ color:{INK}; }}
.card.acc {{ background:{CREAM}; border-color:#F0E2D2; }}
.card.blue{{ background:{BLUE_BG}; border-color:#DCE6FB; }}

/* ── tables ── */
table.tbl {{ width:100%; border-collapse:separate; border-spacing:0; font-size:8.2pt;
            border:1px solid {HAIR}; border-radius:11px; overflow:hidden; }}
table.tbl thead th {{ background:{INK}; color:#fff; font-family:'Sora'; font-weight:600;
            text-align:left; padding:8px 11px; font-size:8pt; letter-spacing:.2px; }}
table.tbl tbody td {{ padding:7px 11px; border-top:1px solid {HAIR}; line-height:1.4; vertical-align:top; color:{INK_SOFT}; }}
table.tbl tbody tr:nth-child(even) td {{ background:#FBFCFE; }}
table.tbl td b {{ color:{INK}; font-weight:700; }}
table.tbl td.tag {{ color:{ACCENT_D}; font-weight:700; white-space:nowrap; }}
.mono {{ font-family:'JetBrains Mono',monospace; font-size:7.6pt; }}

/* ── callouts ── */
.callout {{ border-radius:11px; padding:11px 13px; display:flex; gap:10px; font-size:8.4pt; line-height:1.5; }}
.callout .ic {{ font-size:13pt; line-height:1.2; flex-shrink:0; }}
.callout b {{ font-weight:700; }}
.co-warn {{ background:{AMBER_BG}; border:1px solid #FCEFC7; color:#92400E; }}
.co-warn b{{ color:#78350F; }}
.co-info {{ background:{BLUE_BG}; border:1px solid #DCE6FB; color:#1E40AF; }}
.co-info b{{ color:#1E3A8A; }}
.co-tip  {{ background:{GREEN_BG}; border:1px solid #C7F0DC; color:#065F46; }}
.co-tip b {{ color:#064E3B; }}
.co-danger{{ background:{RED_BG}; border:1px solid #FBD5D5; color:#991B1B; }}
.co-danger b{{ color:#7F1D1D; }}

/* ── lists ── */
.ul {{ display:flex; flex-direction:column; gap:6px; }}
.ul .li {{ display:flex; gap:9px; font-size:8.6pt; line-height:1.45; color:{INK_SOFT}; }}
.ul .li .m {{ flex-shrink:0; width:18px; height:18px; border-radius:6px; background:{CREAM};
             color:{ACCENT_D}; font-size:8pt; font-weight:800; display:flex; align-items:center;
             justify-content:center; font-family:'Sora'; margin-top:1px; }}
.ul.check .li .m {{ background:{GREEN_BG}; color:{GREEN}; }}
.ul .li b {{ color:{INK}; font-weight:700; }}

/* ── mermaid diagram frame ── */
.dgram {{ border:1px solid {HAIR}; border-radius:14px; overflow:hidden; background:#fff;
         display:flex; flex-direction:column; }}
.dgram-hd {{ display:flex; align-items:center; justify-content:space-between;
            padding:8px 13px; background:{INK}; color:#fff; }}
.dgram-hd .t {{ font-family:'Sora'; font-size:9pt; font-weight:600; display:flex; align-items:center; gap:7px; }}
.dgram-hd .t .dot {{ width:8px; height:8px; border-radius:50%; background:{ACCENT}; }}
.dgram-hd .k {{ font-size:7pt; font-weight:600; letter-spacing:.5px; text-transform:uppercase;
               color:#94A3B8; }}
.dgram-canvas {{ flex:1; display:flex; align-items:center; justify-content:center;
                padding:12px; background:radial-gradient(circle at 50% 0,#FBFCFE,#fff); min-height:0; overflow:hidden; }}
.dgram-canvas .mermaid {{ width:100%; height:100%; display:flex; align-items:center; justify-content:center; text-align:center; }}
.dgram-canvas svg {{ max-width:100% !important; max-height:100% !important; width:auto !important; height:auto !important; }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 14px; padding:8px 13px; border-top:1px solid {HAIR}; background:#FBFCFE; }}
.legend .lg {{ display:flex; align-items:center; gap:6px; font-size:7.4pt; color:{MUTE}; font-weight:600; }}
.legend .sw {{ width:11px; height:11px; border-radius:3px; }}

/* ── diagram dossier (eraser + components + layout) ── */
.dossier {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
.dpanel {{ border:1px solid {HAIR}; border-radius:11px; padding:10px 12px; background:#fff; }}
.dpanel.full {{ grid-column:1 / -1; }}
.dpanel-h {{ font-family:'Sora'; font-size:8pt; font-weight:700; text-transform:uppercase;
            letter-spacing:.7px; color:{ACCENT}; margin-bottom:6px; display:flex; align-items:center; gap:6px; }}
.dpanel-h.blue {{ color:{BLUE}; }}
.dpanel-h.violet {{ color:{VIOLET}; }}
.dpanel pre {{ font-family:'JetBrains Mono',monospace; font-size:7pt; line-height:1.55;
              color:{INK_SOFT}; white-space:pre-wrap; }}
.dpanel .comp {{ display:flex; gap:8px; font-size:7.8pt; line-height:1.4; padding:3px 0; }}
.dpanel .comp b {{ color:{INK}; min-width:78px; display:inline-block; }}
.dpanel p {{ font-size:7.9pt; line-height:1.5; color:{INK_SOFT}; }}
.dpanel p b {{ color:{INK}; }}

/* ── Q & A ── */
.qa {{ display:flex; flex-direction:column; gap:9px; }}
.qa-item {{ border:1px solid {HAIR}; border-radius:11px; overflow:hidden; }}
.qa-q {{ background:{CREAM}; padding:8px 12px; font-family:'Sora'; font-size:8.6pt; font-weight:700;
        color:{INK}; display:flex; gap:8px; align-items:flex-start; }}
.qa-q .qm {{ color:{ACCENT}; font-weight:800; }}
.qa-a {{ padding:9px 12px; font-size:8.3pt; line-height:1.5; color:{INK_SOFT}; }}
.qa-a b {{ color:{INK}; }}
.tags {{ display:flex; flex-wrap:wrap; gap:5px; margin-top:7px; }}
.tag-pill {{ font-size:6.8pt; font-weight:700; color:{BLUE}; background:{BLUE_BG};
            padding:3px 8px; border-radius:20px; letter-spacing:.3px; }}

/* ── tradeoff bars / metric bars ── */
.bars {{ display:flex; flex-direction:column; gap:9px; }}
.bar-row {{ display:grid; grid-template-columns:90px 1fr 42px; align-items:center; gap:10px; }}
.bar-l {{ font-size:8pt; font-weight:700; color:{INK}; }}
.bar-track {{ height:13px; background:#F1F5F9; border-radius:7px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:7px; background:linear-gradient(90deg,{ACCENT},{ACCENT_D}); }}
.bar-fill.b {{ background:linear-gradient(90deg,{BLUE},#1E40AF); }}
.bar-fill.g {{ background:linear-gradient(90deg,{GREEN},#047857); }}
.bar-v {{ font-size:8pt; font-weight:700; color:{MUTE}; text-align:right; }}

/* ── timeline ── */
.tl {{ display:flex; flex-direction:column; gap:0; }}
.tl-item {{ display:grid; grid-template-columns:22px 1fr; gap:12px; padding-bottom:13px; position:relative; }}
.tl-item::before {{ content:""; position:absolute; left:10px; top:20px; bottom:0; width:2px; background:{HAIR}; }}
.tl-item:last-child::before {{ display:none; }}
.tl-dot {{ width:22px; height:22px; border-radius:50%; background:{CREAM}; border:2px solid {ACCENT};
          display:flex; align-items:center; justify-content:center; font-family:'Sora'; font-weight:800;
          font-size:8pt; color:{ACCENT_D}; z-index:1; }}
.tl-c h4 {{ font-family:'Sora'; font-size:9pt; font-weight:700; color:{INK}; }}
.tl-c p {{ font-size:8.2pt; line-height:1.45; color:{INK_SOFT}; margin-top:2px; }}

/* ── revision grid ── */
.rev {{ display:grid; grid-template-columns:1fr 1fr; gap:9px; }}
.rev-c {{ border:1px solid {HAIR}; border-radius:10px; padding:9px 11px; background:#fff; }}
.rev-c.acc {{ background:{CREAM}; border-color:#F0E2D2; }}
.rev-h {{ font-family:'Sora'; font-size:8pt; font-weight:700; text-transform:uppercase;
         letter-spacing:.6px; color:{ACCENT}; margin-bottom:4px; }}
.rev-c p {{ font-size:7.9pt; line-height:1.45; color:{INK_SOFT}; }}
.rev-c p b {{ color:{INK}; }}

/* ── two-column split ── */
.split {{ display:grid; grid-template-columns:1fr 1fr; gap:11px; align-items:start; }}
.col {{ display:flex; flex-direction:column; gap:10px; }}
.section-label {{ font-family:'Sora'; font-size:8pt; font-weight:700; text-transform:uppercase;
                 letter-spacing:.8px; color:{ACCENT}; display:flex; align-items:center; gap:7px; }}
.section-label::after {{ content:""; flex:1; height:1px; background:{HAIR}; }}

/* ── code block ── */
.code {{ background:{INK}; border-radius:11px; padding:11px 13px; overflow:hidden; }}
.code pre {{ font-family:'JetBrains Mono',monospace; font-size:7.4pt; line-height:1.6; color:#E2E8F0; white-space:pre-wrap; }}
.code .cm {{ color:#64748B; }} .code .kw {{ color:#FBBF24; }} .code .fn {{ color:#60A5FA; }} .code .st {{ color:#86EFAC; }}
.code-cap {{ font-size:7.4pt; color:{MUTE}; margin-top:5px; }}

/* ── cover ── */
.cover {{ background:radial-gradient(1200px 700px at 75% -10%,#1E293B,#0B1120 60%); color:#fff;
         justify-content:space-between; padding:0; }}
.cover::after {{ content:""; position:absolute; inset:0;
  background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
  background-size:26px 26px; pointer-events:none; }}
.cv-top {{ padding:20mm 18mm 0; position:relative; z-index:2; display:flex; align-items:center; justify-content:space-between; }}
.cv-brand {{ display:flex; align-items:center; gap:11px; }}
.cv-brand img {{ height:30px; }}
.cv-brand .w {{ font-family:'Sora'; font-weight:800; font-size:16pt; letter-spacing:-.3px; }}
.cv-brand .w span {{ color:{ACCENT}; }}
.cv-edition {{ font-size:8pt; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#64748B;
              border:1px solid #334155; border-radius:20px; padding:6px 13px; }}
.cv-mid {{ padding:0 18mm; position:relative; z-index:2; }}
.cv-kicker {{ font-family:'Sora'; font-size:10pt; font-weight:700; letter-spacing:3px; text-transform:uppercase;
             color:{ACCENT}; margin-bottom:16px; }}
.cv-title {{ font-family:'Sora'; font-size:46pt; font-weight:800; line-height:1.02; letter-spacing:-2px; }}
.cv-title .accent {{ background:linear-gradient(90deg,{ACCENT},#F59E0B); -webkit-background-clip:text;
                    background-clip:text; -webkit-text-fill-color:transparent; }}
.cv-sub {{ font-size:13pt; color:#94A3B8; font-weight:500; margin-top:20px; max-width:150mm; line-height:1.5; }}
.cv-tags {{ display:flex; flex-wrap:wrap; gap:9px; margin-top:26px; }}
.cv-tag {{ font-size:8.5pt; font-weight:600; color:#CBD5E1; background:rgba(255,255,255,.06);
          border:1px solid #334155; border-radius:8px; padding:7px 13px; }}
.cv-tag b {{ color:{ACCENT}; }}
.cv-bot {{ padding:0 18mm 18mm; position:relative; z-index:2; display:flex; align-items:flex-end; justify-content:space-between; }}
.cv-stats {{ display:flex; gap:30px; }}
.cv-stat .n {{ font-family:'Sora'; font-size:24pt; font-weight:800; color:#fff; line-height:1; }}
.cv-stat .n span {{ color:{ACCENT}; }}
.cv-stat .l {{ font-size:7.5pt; color:#64748B; text-transform:uppercase; letter-spacing:1px; margin-top:5px; font-weight:600; }}
.cv-foot {{ text-align:right; font-size:8pt; color:#475569; line-height:1.6; }}
.cv-foot b {{ color:#94A3B8; }}

/* ── TOC ── */
.toc-wrap {{ display:grid; grid-template-columns:1fr 1fr; gap:9px 24px; }}
.toc-row {{ display:flex; align-items:baseline; gap:8px; font-size:8.6pt; padding:3px 0; }}
.toc-n {{ font-family:'Sora'; font-weight:800; font-size:8pt; color:{ACCENT}; min-width:20px; }}
.toc-t {{ color:{INK_SOFT}; font-weight:500; }}
.toc-t b {{ color:{INK}; font-weight:700; }}
.toc-dots {{ flex:1; border-bottom:1px dotted {HAIR}; transform:translateY(-3px); }}
.toc-section-h {{ font-family:'Sora'; font-size:9pt; font-weight:800; color:{INK}; text-transform:uppercase;
                 letter-spacing:1px; margin:6px 0 2px; grid-column:1/-1; display:flex; align-items:center; gap:9px; }}
.toc-section-h .b {{ width:18px; height:3px; border-radius:2px; background:{ACCENT}; }}

/* divider band */
.band {{ background:linear-gradient(120deg,{INK},#1E293B); color:#fff; justify-content:center; padding:0 22mm; }}
.band::after {{ content:""; position:absolute; inset:0;
  background-image:radial-gradient(circle at 80% 20%,rgba(234,118,63,.18),transparent 45%); }}
.band-n {{ font-family:'Sora'; font-size:120pt; font-weight:800; color:rgba(255,255,255,.06); line-height:.8; letter-spacing:-4px; }}
.band-k {{ font-family:'Sora'; font-size:10pt; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:{ACCENT}; position:relative; z-index:2; margin-bottom:10px; }}
.band-t {{ font-family:'Sora'; font-size:34pt; font-weight:800; letter-spacing:-1px; position:relative; z-index:2; line-height:1.05; }}
.band-s {{ font-size:11pt; color:#94A3B8; margin-top:14px; max-width:140mm; line-height:1.5; position:relative; z-index:2; }}
.band-meta {{ display:flex; gap:26px; margin-top:26px; position:relative; z-index:2; }}
.band-meta .m .n {{ font-family:'Sora'; font-size:17pt; font-weight:800; color:{ACCENT}; }}
.band-meta .m .l {{ font-size:7.5pt; color:#64748B; text-transform:uppercase; letter-spacing:1px; margin-top:3px; }}
"""

# ──────────────────────────────────────────────────────────────────────────────
# BLOCK RENDERERS  — each returns an HTML fragment
# ──────────────────────────────────────────────────────────────────────────────
def b_lead(text):
    return f'<p class="lead">{text}</p>'

def b_kpis(items, cols=None):
    cols = cols or len(items)
    cells = "".join(
        f'<div class="kpi {it.get("c","")}"><div class="kpi-v">{esc(it["v"])}</div>'
        f'<div class="kpi-l">{esc(it["l"])}</div></div>' for it in items)
    return f'<div class="kpis" style="grid-template-columns:repeat({cols},1fr);">{cells}</div>'

def b_cards(items, cols=2):
    cells = ""
    for it in items:
        cls = it.get("cls","")
        ic = f'<div class="card-ic">{it["ic"]}</div>' if it.get("ic") else ""
        cells += (f'<div class="card {cls}">{ic}<div class="card-h">{esc(it["h"])}</div>'
                  f'<div class="card-p">{it["p"]}</div></div>')
    return f'<div class="cards" style="grid-template-columns:repeat({cols},1fr);">{cells}</div>'

def b_table(head, rows, tagcol=None):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    trs = ""
    for r in rows:
        tds = ""
        for i, c in enumerate(r):
            cls = ' class="tag"' if tagcol is not None and i == tagcol else ""
            tds += f"<td{cls}>{c}</td>"
        trs += f"<tr>{tds}</tr>"
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def b_callout(kind, title, text, ic=None):
    icons = {"warn":"⚠️","info":"ℹ️","tip":"✅","danger":"🛑"}
    ic = ic or icons.get(kind,"•")
    return (f'<div class="callout co-{kind}"><div class="ic">{ic}</div>'
            f'<div><b>{esc(title)}</b> — {text}</div></div>')

def b_list(items, style="num", title=None):
    rows = ""
    for i, it in enumerate(items):
        m = "✓" if style == "check" else (str(i+1) if style == "num" else "›")
        rows += f'<div class="li"><div class="m">{m}</div><div>{it}</div></div>'
    head = f'<div class="section-label">{esc(title)}</div>' if title else ""
    return f'{head}<div class="ul {style}">{rows}</div>'

def b_label(text):
    return f'<div class="section-label">{esc(text)}</div>'

_MM_HEADERS = ("flowchart","graph","sequenceDiagram","erDiagram","classDiagram",
               "stateDiagram","journey","gantt","pie","mindmap")
def _normalize_mermaid(code):
    """Ensure the diagram-type directive is the first line; classDef/style lines
    may be authored before it for convenience — we hoist the directive up."""
    lines = code.strip("\n").split("\n")
    hdr_idx = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if any(s.startswith(h) for h in _MM_HEADERS):
            hdr_idx = i; break
    if hdr_idx in (None, 0):
        return code.strip()
    hdr = lines.pop(hdr_idx)
    return "\n".join([hdr] + lines).strip()

def _mermaid(code, mid):
    return f'<div class="dgram-canvas"><pre class="mermaid" id="{mid}">{_normalize_mermaid(code)}</pre></div>'

def b_diagram(d):
    """A framed Mermaid diagram with header + optional legend."""
    mid = d.get("id","d")
    kind = d.get("kind","ARCHITECTURE")
    legend = ""
    if d.get("legend"):
        lgs = "".join(f'<div class="lg"><span class="sw" style="background:{c}"></span>{esc(l)}</div>'
                      for c,l in d["legend"])
        legend = f'<div class="legend">{lgs}</div>'
    return (f'<div class="dgram" style="flex:1; min-height:0;">'
            f'<div class="dgram-hd"><div class="t"><span class="dot"></span>{esc(d["title"])}</div>'
            f'<div class="k">{esc(kind)}</div></div>'
            f'{_mermaid(d["code"], mid)}{legend}</div>')

def b_dossier(d):
    """Eraser spec + component breakdown + visual layout — the 4-part diagram spec."""
    comps = "".join(f'<div class="comp"><b>{esc(n)}</b><span>{t}</span></div>' for n,t in d.get("components",[]))
    eraser = esc(d.get("eraser","")) if d.get("eraser") else ""
    layout = d.get("layout","")
    out = '<div class="dossier">'
    if eraser:
        out += (f'<div class="dpanel"><div class="dpanel-h">⬡ Eraser Diagram Spec</div>'
                f'<pre>{eraser}</pre></div>')
    if comps:
        out += (f'<div class="dpanel"><div class="dpanel-h blue">▣ Component Breakdown</div>{comps}</div>')
    if layout:
        out += (f'<div class="dpanel full"><div class="dpanel-h violet">◳ Visual Layout Description</div>'
                f'<p>{layout}</p></div>')
    out += '</div>'
    return out

def b_qa(items):
    out = '<div class="qa">'
    for it in items:
        tags = ""
        if it.get("tags"):
            tags = '<div class="tags">' + "".join(f'<span class="tag-pill">{esc(t)}</span>' for t in it["tags"]) + '</div>'
        out += (f'<div class="qa-item"><div class="qa-q"><span class="qm">Q</span>{esc(it["q"])}</div>'
                f'<div class="qa-a">{it["a"]}{tags}</div></div>')
    return out + '</div>'

def b_bars(items, title=None):
    rows = ""
    for it in items:
        cls = it.get("c","")
        rows += (f'<div class="bar-row"><div class="bar-l">{esc(it["l"])}</div>'
                 f'<div class="bar-track"><div class="bar-fill {cls}" style="width:{it["pct"]}%"></div></div>'
                 f'<div class="bar-v">{esc(it.get("v",""))}</div></div>')
    head = b_label(title) if title else ""
    return f'{head}<div class="bars">{rows}</div>'

def b_timeline(items):
    rows = ""
    for i, it in enumerate(items):
        rows += (f'<div class="tl-item"><div class="tl-dot">{esc(it.get("n",str(i+1)))}</div>'
                 f'<div class="tl-c"><h4>{esc(it["h"])}</h4><p>{it["p"]}</p></div></div>')
    return f'<div class="tl">{rows}</div>'

def b_revision(items):
    cells = ""
    for it in items:
        cls = "acc" if it.get("acc") else ""
        cells += f'<div class="rev-c {cls}"><div class="rev-h">{esc(it["h"])}</div><p>{it["p"]}</p></div>'
    return f'<div class="rev">{cells}</div>'

def b_code(code, cap=None):
    capx = f'<div class="code-cap">{esc(cap)}</div>' if cap else ""
    return f'<div class="code"><pre>{code}</pre></div>{capx}'

def b_split(left, right):
    L = "".join(left); R = "".join(right)
    return f'<div class="split"><div class="col">{L}</div><div class="col">{R}</div></div>'

# ──────────────────────────────────────────────────────────────────────────────
# PAGE ASSEMBLY
# ──────────────────────────────────────────────────────────────────────────────
def _header(meta, page):
    badge = page.get("badge")
    badge_html = ""
    if badge:
        bcls = badge.get("cls","chip-acc")
        badge_html = f'<span class="chip {bcls}">{esc(badge["t"])}</span>'
    return (f'<div class="rh"><div class="rh-l">'
            f'<img src="data:image/png;base64,{LOGO_B64}"/>'
            f'<div class="rh-wm">Grind<span>OS</span></div></div>'
            f'<div class="rh-r"><span class="chip chip-mute">{esc(meta["running"])}</span>{badge_html}</div></div>')

def _footer(meta, page):
    pn = page.get("pageno","")
    return (f'<div class="rf"><div>{esc(meta["footer_l"])}</div>'
            f'<div><b>{esc(page.get("foot_mid",""))}</b></div>'
            f'<div>{esc(meta["book"])} · <b>{pn}</b></div></div>')

def _mast(page):
    eyebrow = page.get("eyebrow","")
    yield_h = ""
    if page.get("yield"):
        stars = "★"*page["yield"] + "☆"*(5-page["yield"])
        yield_h = f'<div class="mast-yield">Interview Yield <b>{stars}</b></div>'
    return (f'<div class="mast"><div class="mast-top">'
            f'<div class="mast-eyebrow">{esc(eyebrow)}</div>'
            f'{yield_h}</div>'
            f'<div class="mast-top" style="align-items:flex-end;">'
            f'<div><div class="mast-title">{esc(page["title"])}</div>'
            f'<div class="mast-sub">{esc(page.get("sub",""))}</div></div>'
            f'<div class="mast-num">{esc(page.get("num",""))}</div></div></div>')

def render_content_page(meta, page):
    body = "".join(page["blocks"])
    return (f'<div class="page">{_header(meta,page)}{_mast(page)}'
            f'<div class="body">{body}</div>{_footer(meta,page)}</div>')

def render_cover(meta, c):
    tags = "".join(f'<div class="cv-tag">{t}</div>' for t in c["tags"])
    stats = "".join(f'<div class="cv-stat"><div class="n">{n}</div><div class="l">{esc(l)}</div></div>'
                    for n,l in c["stats"])
    return (f'<div class="page cover">'
            f'<div class="cv-top"><div class="cv-brand">'
            f'<img src="data:image/png;base64,{LOGO_B64}"/><div class="w">Grind<span>OS</span></div></div>'
            f'<div class="cv-edition">{esc(c["edition"])}</div></div>'
            f'<div class="cv-mid"><div class="cv-kicker">{esc(c["kicker"])}</div>'
            f'<div class="cv-title">{c["title"]}</div>'
            f'<div class="cv-sub">{esc(c["sub"])}</div>'
            f'<div class="cv-tags">{tags}</div></div>'
            f'<div class="cv-bot"><div class="cv-stats">{stats}</div>'
            f'<div class="cv-foot">{c["foot"]}</div></div></div>')

def render_band(meta, b):
    meta_h = ""
    if b.get("meta"):
        meta_h = '<div class="band-meta">' + "".join(
            f'<div class="m"><div class="n">{n}</div><div class="l">{esc(l)}</div></div>'
            for n,l in b["meta"]) + '</div>'
    return (f'<div class="page band">'
            f'<div class="band-n" style="position:absolute; top:30mm; right:18mm;">{esc(b.get("bignum",""))}</div>'
            f'<div class="band-k">{esc(b["kicker"])}</div>'
            f'<div class="band-t">{b["title"]}</div>'
            f'<div class="band-s">{esc(b["sub"])}</div>{meta_h}</div>')

def render_toc(meta, t):
    out = '<div class="toc-wrap">'
    for grp in t["groups"]:
        out += f'<div class="toc-section-h"><span class="b"></span>{esc(grp["h"])}</div>'
        for n, title in grp["rows"]:
            out += (f'<div class="toc-row"><span class="toc-n">{esc(n)}</span>'
                    f'<span class="toc-t">{title}</span><span class="toc-dots"></span></div>')
    out += '</div>'
    page = {"eyebrow":t.get("eyebrow","Contents"), "title":t["title"], "sub":t.get("sub",""),
            "num":t.get("num","00"), "pageno":t.get("pageno",""), "running":meta["running"]}
    return (f'<div class="page">{_header(meta,page)}{_mast(page)}'
            f'<div class="body">{out}</div>{_footer(meta,page)}</div>')

# ──────────────────────────────────────────────────────────────────────────────
# DOCUMENT SHELL  (+ Mermaid runtime, themed on-brand)
# ──────────────────────────────────────────────────────────────────────────────
def _mermaid_runtime():
    return f"""
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad:true, securityLevel:'loose',
    theme:'base', fontFamily:'Inter, sans-serif',
    themeVariables:{{
      fontSize:'13px',
      primaryColor:'{CREAM}', primaryBorderColor:'{ACCENT}', primaryTextColor:'{INK}',
      lineColor:'{MUTE}', textColor:'{INK_SOFT}',
      secondaryColor:'{BLUE_BG}', tertiaryColor:'{GREEN_BG}',
      clusterBkg:'#FBFCFE', clusterBorder:'{HAIR}',
      actorBkg:'{CREAM}', actorBorder:'{ACCENT}', actorTextColor:'{INK}',
      signalColor:'{INK_SOFT}', signalTextColor:'{INK}',
      labelBoxBkgColor:'{BLUE_BG}', labelBoxBorderColor:'{BLUE}',
      noteBkgColor:'{AMBER_BG}', noteBorderColor:'{AMBER}', noteTextColor:'#78350F',
      sequenceNumberColor:'#fff'
    }},
    flowchart:{{ curve:'basis', htmlLabels:true, padding:10, nodeSpacing:42, rankSpacing:46 }},
    sequence:{{ actorMargin:46, boxMargin:8, mirrorActors:false, messageFontWeight:500 }}
  }});
</script>"""

def render_book(meta, pages):
    parts = []
    for pg in pages:
        k = pg["kind"]
        if   k == "cover":   parts.append(render_cover(meta, pg))
        elif k == "band":    parts.append(render_band(meta, pg))
        elif k == "toc":     parts.append(render_toc(meta, pg))
        elif k == "content": parts.append(render_content_page(meta, pg))
    body = "\n".join(parts)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<title>{esc(meta["title"])}</title><style>{_css()}</style></head>'
            f'<body>{body}{_mermaid_runtime()}</body></html>')
