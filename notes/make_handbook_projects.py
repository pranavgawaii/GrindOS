"""
GrindOS — PROJECTS & ARCHITECTURE HANDBOOK  (Premium Edition)
=============================================================
Rebuilt from first principles on the block-based engine. Every project gets a
22-section flagship treatment plus 7 professional Mermaid diagrams, each shipped
as a 4-part spec: Eraser diagram, Mermaid code, Component breakdown, Visual layout.

Run:  python3 make_handbook_projects.py
Out:  subjects/projects/01_projects.html   (build.py -> PDF via Playwright)
"""
import os
from handbook_engine import *
from handbook_engine import _HERE

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION BUILDER  — turns a project dict into 22 premium pages
# ══════════════════════════════════════════════════════════════════════════════
SECTION_TITLES = [
    ("01","Executive Summary"),("02","Product Vision"),("03","Business Problem"),
    ("04","User Journey"),("05","Functional Requirements"),("06","Non-Functional Requirements"),
    ("07","Tech Stack Decisions"),("08","Architecture Overview"),("09","Request Lifecycle"),
    ("10","Database Design"),("11","Authentication Design"),("12","Deployment Architecture"),
    ("13","Scalability Architecture"),("14","Security Architecture"),("15","Failure Recovery"),
    ("16","Monitoring & Observability"),("17","Cost Optimization"),("18","Engineering Challenges"),
    ("19","Architecture Tradeoffs"),("20","Future Roadmap"),("21","Interview Deep Dive"),
    ("22","Revision Sheet"),
]

def _pg(p, num, title, blocks, sub="", yld=4, badge=None):
    return {"kind":"content","eyebrow":f'{p["name"]} · Section {num}',"num":num,
            "title":title,"sub":sub or p["tagline"],"yield":yld,
            "running":p["name"],"pageno":"","blocks":blocks,
            "badge":badge or {"cls":"chip-acc","t":p["tagline"]}}

def build_project(p):
    pages = []
    nm = p["name"]
    # ── band divider ──
    pages.append({"kind":"band","kicker":f'Project Dossier · {p["pnum"]}',
                  "title":nm, "bignum":p["pnum"], "sub":p["subtitle"],
                  "meta":p["band_meta"]})

    f = p["fields"]
    D = p["diagrams"]

    # 01 EXECUTIVE SUMMARY
    pages.append(_pg(p,"01","Executive Summary",[
        b_lead(f["summary_lead"]),
        b_kpis(f["kpis"], cols=4),
        b_cards([
            {"ic":"🚨","h":"The Core Problem","p":f["problem"],"cls":""},
            {"ic":"👥","h":"Target Users & Value","p":f["users"],"cls":""},
            {"ic":"🎯","h":"Business Goal & Impact","p":f["goal"],"cls":"acc"},
            {"ic":"👑","h":"My Role & Ownership","p":f["role"],"cls":"acc"},
        ], cols=2),
    ], sub="What it is, who it serves, why it matters", yld=5))

    # 02 PRODUCT VISION
    pages.append(_pg(p,"02","Product Vision",[
        b_lead(f["vision_lead"]),
        b_label("Alternatives We Rejected"),
        b_table(["Alternative","Where It Breaks",f"{nm} Edge"], f["alternatives"], tagcol=0),
        b_label("Core Capability Matrix"),
        b_cards(f["features_cards"], cols=3),
    ], sub="The bet, the wedge, the moat"))

    # 03 BUSINESS PROBLEM
    pages.append(_pg(p,"03","Business Problem",[
        b_lead(f["biz_lead"]),
        b_cards(f["pain_cards"], cols=2),
        b_callout("info","Why now", f["why_now"]),
        b_bars(f["impact_bars"], title="Cost of the Status Quo"),
    ], sub="Quantifying the pain we remove", yld=3))

    # 04 USER JOURNEY
    pages.append(_pg(p,"04","User Journey",[
        b_lead(f["journey_lead"]),
        b_timeline(f["journey"]),
    ], sub="From first touch to recurring value"))

    # 05 FUNCTIONAL REQUIREMENTS
    pages.append(_pg(p,"05","Functional Requirements",[
        b_lead("Scoped to the critical path. Each requirement maps to an owned subsystem and an acceptance signal."),
        b_split(
            [b_list(f["fr_must"], style="check", title="Must-Have (P0)")],
            [b_list(f["fr_should"], style="bullet", title="Should-Have (P1)")],
        ),
        b_table(["ID","Capability","Acceptance Signal"], f["fr_table"], tagcol=0),
    ], sub="P0 / P1 capability contract", yld=3))

    # 06 NON-FUNCTIONAL REQUIREMENTS
    pages.append(_pg(p,"06","Non-Functional Requirements",[
        b_lead("The quality attributes that define production-readiness — each with a measurable target and the mechanism that enforces it."),
        b_table(["Attribute","Target (SLO)","Enforcement Mechanism"], f["nfr_table"], tagcol=0),
        b_bars(f["nfr_bars"], title="Quality Attribute Priority"),
    ], sub="SLOs, not vibes", yld=5))

    # 07 TECH STACK DECISIONS
    pages.append(_pg(p,"07","Tech Stack Decisions",[
        b_lead(f["stack_lead"]),
        b_table(["Layer","Chosen","Why This","Trade-off Accepted"], f["stack_table"], tagcol=0),
    ], sub="Every choice has a bill", yld=4))

    # 08 ARCHITECTURE OVERVIEW  (Diagram 1)
    pages.append(_pg(p,"08","Architecture Overview",[
        b_diagram(D["arch"]),
        b_dossier(D["arch"]),
    ], sub="Diagram 1 — System Architecture", yld=5,
       badge={"cls":"chip-blue","t":"Diagram 1 / 7"}))

    # 09 REQUEST LIFECYCLE  (Diagram 2)
    pages.append(_pg(p,"09","Request Lifecycle",[
        b_diagram(D["flow"]),
        b_dossier(D["flow"]),
    ], sub="Diagram 2 — End-to-End Request Flow", yld=5,
       badge={"cls":"chip-blue","t":"Diagram 2 / 7"}))

    # 10 DATABASE DESIGN  (Diagram 3 — ERD)
    pages.append(_pg(p,"10","Database Design",[
        b_diagram(D["erd"]),
        b_dossier(D["erd"]),
    ], sub="Diagram 3 — Entity Relationship Model", yld=4,
       badge={"cls":"chip-blue","t":"Diagram 3 / 7"}))

    # 11 AUTHENTICATION DESIGN  (Diagram 4)
    pages.append(_pg(p,"11","Authentication Design",[
        b_diagram(D["auth"]),
        b_dossier(D["auth"]),
    ], sub="Diagram 4 — Identity & Authorization Flow", yld=4,
       badge={"cls":"chip-blue","t":"Diagram 4 / 7"}))

    # 12 DEPLOYMENT ARCHITECTURE  (Diagram 5)
    pages.append(_pg(p,"12","Deployment Architecture",[
        b_diagram(D["deploy"]),
        b_dossier(D["deploy"]),
    ], sub="Diagram 5 — Cloud Deployment Topology", yld=4,
       badge={"cls":"chip-blue","t":"Diagram 5 / 7"}))

    # 13 SCALABILITY ARCHITECTURE  (Diagram 6)
    pages.append(_pg(p,"13","Scalability Architecture",[
        b_diagram(D["scale"]),
        b_table(["Scale","First Bottleneck","Architectural Move"], f["scale_table"], tagcol=0),
    ], sub="Diagram 6 — Scaling Evolution 100 → 1M", yld=5,
       badge={"cls":"chip-blue","t":"Diagram 6 / 7"}))

    # 14 SECURITY ARCHITECTURE
    pages.append(_pg(p,"14","Security Architecture",[
        b_lead(f["sec_lead"]),
        b_table(["Threat (STRIDE)","Vector","Mitigation"], f["threats"], tagcol=0),
        b_callout("danger", f["sec_callout"][0], f["sec_callout"][1]),
    ], sub="Threat model & controls", yld=4))

    # 15 FAILURE RECOVERY  (Diagram 7)
    pages.append(_pg(p,"15","Failure Recovery",[
        b_diagram(D["failure"]),
        b_dossier(D["failure"]),
    ], sub="Diagram 7 — Failure & Recovery Topology", yld=5,
       badge={"cls":"chip-blue","t":"Diagram 7 / 7"}))

    # 16 MONITORING
    pages.append(_pg(p,"16","Monitoring & Observability",[
        b_lead("Instrumented around the four golden signals. Every alert is actionable and maps to a runbook."),
        b_cards(f["golden"], cols=4),
        b_label("Alerting Matrix"),
        b_table(["Signal","Threshold","Action / Runbook"], f["alerts"], tagcol=0),
    ], sub="Golden signals + alert matrix", yld=3))

    # 17 COST OPTIMIZATION
    pages.append(_pg(p,"17","Cost Optimization",[
        b_lead(f["cost_lead"]),
        b_kpis(f["cost_kpis"], cols=3),
        b_list(f["cost_moves"], style="check", title="Levers Pulled"),
    ], sub="Unit economics under load", yld=3))

    # 18 ENGINEERING CHALLENGES
    pages.append(_pg(p,"18","Engineering Challenges",[
        b_label("Production Incident — Post-Mortem"),
        b_cards([
            {"ic":"🔥","h":"The Incident","p":f["incident"][0]},
            {"ic":"🔎","h":"Root Cause","p":f["incident"][1]},
            {"ic":"🛠️","h":"The Fix","p":f["incident"][2],"cls":"acc"},
            {"ic":"📈","h":"Lasting Lesson","p":f["incident"][3],"cls":"acc"},
        ], cols=2),
        b_callout("warn", "Blast radius", f["incident_blast"]),
    ], sub="What broke, why, and what we learned", yld=5))

    # 19 ARCHITECTURE TRADEOFFS
    pages.append(_pg(p,"19","Architecture Tradeoffs",[
        b_lead("Every architecture is a set of deliberate sacrifices. Here are the ones we made on purpose — and what we gave up."),
        b_table(["Decision","We Chose","We Sacrificed"], f["tradeoffs"], tagcol=0),
        b_bars(f["tradeoff_bars"], title="Where We Optimized"),
    ], sub="Chosen sacrifices, stated plainly", yld=5))

    # 20 FUTURE ROADMAP
    pages.append(_pg(p,"20","Future Roadmap",[
        b_lead(f["roadmap_lead"]),
        b_timeline(f["roadmap"]),
    ], sub="Where the architecture goes next", yld=2))

    # 21 INTERVIEW DEEP DIVE
    pages.append(_pg(p,"21","Interview Deep Dive",[
        b_qa(f["qa"]),
    ], sub="The questions that decide the loop", yld=5))

    # 22 REVISION SHEET
    pages.append(_pg(p,"22","Revision Sheet",[
        b_lead(f["rev_lead"]),
        b_revision(f["revision"]),
        b_callout("tip","60-second pitch", f["pitch"]),
    ], sub="One-page recall before the round", yld=5))

    return pages

# ══════════════════════════════════════════════════════════════════════════════
#  FRONT MATTER
# ══════════════════════════════════════════════════════════════════════════════
def front_matter(projects):
    cover = {"kind":"cover","edition":"2026 Edition · v2",
        "kicker":"GrindOS Engineering Library",
        "title":'Projects &amp;<br><span class="accent">Architecture</span><br>Handbook',
        "sub":"Seven production systems, reverse-engineered into interview-ready architecture dossiers. "
              "Diagrams, trade-offs, failure modes, and the exact answers that pass the loop.",
        "tags":['<b>7</b>&nbsp; Flagship Projects','<b>49</b>&nbsp; Pro Diagrams',
                '<b>22</b>&nbsp; Sections / Project','<b>Mermaid</b> + Eraser Specs','Interview-Grade Depth'],
        "stats":[('<span>7</span>',"Systems"),('<span>49</span>',"Diagrams"),
                 ('<span>165</span>',"Pages"),('<span>FAANG</span>',"Bar")],
        "foot":"GrindOS &middot; Premium Engineering Series<br><b>Visual-first. Interview-ready.</b>"}

    groups = [{"h":"The Seven Systems","rows":[
        (p["pnum"], f'<b>{p["name"]}</b> — {p["tagline"]}') for p in projects]}]
    groups.append({"h":"Every Project Contains","rows":[
        (n, t) for n,t in SECTION_TITLES[:11]]})
    groups.append({"h":"(continued)","rows":[
        (n, t) for n,t in SECTION_TITLES[11:]]})
    toc = {"kind":"toc","title":"Contents","eyebrow":"Navigation",
           "sub":"7 dossiers × 22 sections — diagrams flagged inline","num":"00","groups":groups}

    how = {"kind":"content","eyebrow":"How To Read This Book","num":"·",
        "title":"Reading Protocol","sub":"Built for spaced revision and live interviews",
        "yield":5,"running":"Guide","pageno":"","badge":{"cls":"chip-blue","t":"Start Here"},
        "blocks":[
            b_lead("This is not a notes dump. Every project is a self-contained architecture interview, "
                   "sequenced the way a senior engineer would actually defend a system on a whiteboard."),
            b_cards([
                {"ic":"🧭","h":"Sections 01–07","p":"<b>The Why.</b> Problem, users, requirements, and stack decisions. Establishes the business context an interviewer probes first."},
                {"ic":"🏛️","h":"Sections 08–15","p":"<b>The How.</b> Eight diagram-driven pages: architecture, request flow, ERD, auth, deployment, scaling, security, failure. The core of any design round."},
                {"ic":"🛡️","h":"Sections 16–19","p":"<b>The Hard Parts.</b> Monitoring, cost, real incidents, and the trade-offs you chose on purpose. Where senior signal lives."},
                {"ic":"🎯","h":"Sections 20–22","p":"<b>The Recall.</b> Roadmap, deep-dive Q&amp;A, and a one-page revision sheet for the night before."},
            ], cols=2),
            b_callout("info","Every diagram ships as a 4-part spec",
                "A framed <b>Mermaid</b> render (vector, exportable), an <b>Eraser</b> diagram-as-code block you can paste into eraser.io, a <b>component breakdown</b>, and a <b>visual layout</b> description — so you can redraw it from memory on any whiteboard."),
            b_bars([
                {"l":"Visual recall","pct":95,"v":"●●●●●","c":""},
                {"l":"Interview depth","pct":92,"v":"●●●●●","c":"b"},
                {"l":"Trade-off fluency","pct":90,"v":"●●●●●","c":"g"},
            ], title="What This Book Optimizes"),
        ]}
    return [cover, toc, how]

# ══════════════════════════════════════════════════════════════════════════════
#  PROJECT CONTENT
# ══════════════════════════════════════════════════════════════════════════════
from projects_data import PROJECTS

def main():
    meta = {"title":"GrindOS — Projects & Architecture Handbook",
            "book":"Projects Handbook","running":"Projects",
            "footer_l":"GrindOS Premium Series","subject":"projects"}
    pages = front_matter(PROJECTS)
    for p in PROJECTS:
        pages += build_project(p)
    htmlout = render_book(meta, pages)
    out = os.path.join(_HERE, "subjects/projects/01_projects.html")
    with open(out, "w") as fp:
        fp.write(htmlout)
    print(f"✓ Projects handbook: {len(pages)} pages -> {out}")

if __name__ == "__main__":
    main()
