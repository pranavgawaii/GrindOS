from playwright.sync_api import sync_playwright
import os
html = os.path.abspath("subjects/projects/01_projects.html")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":794,"height":1123}, device_scale_factor=2)
    pg.goto(f"file://{html}")
    pg.wait_for_load_state("networkidle")
    pg.wait_for_timeout(2500)  # let mermaid finish
    # full PDF
    pg.pdf(path="output/GrindOS_PROJECTS_Booklet.pdf", format="A4", print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"})
    # screenshot specific pages: cover(0), arch diagram(section08), erd(section10), failure(section15)
    pages = pg.query_selector_all(".page")
    print("total .page elements:", len(pages))
    for idx in [0, 3, 11, 13, 18]:
        if idx < len(pages):
            pages[idx].scroll_into_view_if_needed()
            pages[idx].screenshot(path=f"_shot_{idx}.png")
    b.close()
print("done")
