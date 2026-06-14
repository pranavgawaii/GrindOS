from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://grindos.pranavx.in/')
        print("Landed on:", page.url)
        
        # Click the Sign In button
        page.click('text="Sign In"')
        page.wait_for_load_state('networkidle')
        print("After clicking Sign In, url is:", page.url)
        
        # See what's on the page
        print("Title:", page.title())
        browser.close()

if __name__ == '__main__':
    run()
