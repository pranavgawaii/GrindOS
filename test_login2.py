from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://grindos.pranavx.in/')
        
        page.click('text="Sign In"')
        page.wait_for_load_state('networkidle')
        
        page.screenshot(path='/Users/8teen/.gemini/antigravity-ide/brain/112d161f-5064-45ef-b097-351e6e4ab7ce/artifacts/screenshot.png')
        browser.close()

if __name__ == '__main__':
    run()
