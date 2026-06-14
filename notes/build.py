from playwright.sync_api import sync_playwright
import glob, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Mapping: subject key -> output booklet name
SUBJECTS = {
    "oops":          "GrindOS_OOPS_Booklet",
    "dbms":          "GrindOS_DBMS_Booklet",
    "os":            "GrindOS_OS_Booklet",
    "cn":            "GrindOS_CN_Booklet",
    "sql":           "GrindOS_SQL_Booklet",
    "system_design": "GrindOS_SYSTEM_DESIGN_Booklet",
    "projects":      "GrindOS_PROJECTS_Booklet",
    "python":        "GrindOS_PYTHON_Booklet",
    "dsa":           "GrindOS_DSA_Booklet",
    "aiml":          "GrindOS_AIML_Booklet",
}

def convert(html_path, pdf_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top":"0","bottom":"0","left":"0","right":"0"}
        )
        browser.close()
        print(f"  ✓ {os.path.basename(pdf_path)}")

# Usage: python build.py oops   OR   python build.py all
subject = sys.argv[1] if len(sys.argv) > 1 else "all"
targets = list(SUBJECTS.keys()) if subject == "all" else [subject]

os.makedirs("output", exist_ok=True)

for subj in targets:
    booklet_name = SUBJECTS.get(subj, f"GrindOS_{subj.upper()}_Booklet")
    html_files = sorted(glob.glob(f"subjects/{subj}/*.html"))
    if not html_files:
        print(f"\n⚠ No HTML files found for {subj.upper()}, skipping.")
        continue

    print(f"\nBuilding {subj.upper()}...")
    # Each subject has a single HTML → single PDF in output/
    for html in html_files:
        out_pdf = f"output/{booklet_name}.pdf"
        convert(html, out_pdf)

print("\nDone.")
