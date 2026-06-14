from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://grindos.pranavx.in/')
        
        page.click('text="Sign In"')
        page.wait_for_load_state('networkidle')
        print("URL right after click:", page.url)
        
        time.sleep(5)
        print("URL after 5 seconds:", page.url)
        
        browser.close()

if __name__ == '__main__':
    run()
