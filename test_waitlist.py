from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Log console messages
        page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))
        
        page.goto('https://grindos.pranavx.in/')
        
        # Open waitlist modal
        page.click('text="Join Waitlist"')
        page.wait_for_selector('#waitlist-email')
        
        # Fill email and submit
        page.fill('#waitlist-email', 'test@example.com')
        page.click('#waitlist-form button[type="submit"]')
        
        # Wait for followup modal
        page.wait_for_selector('#waitlist-followup-form', state='visible')
        
        # Click "Submit & Secure Spot"
        page.click('#wl-submit-btn')
        
        # Wait to see what happens
        page.wait_for_timeout(3000)
        
        browser.close()

if __name__ == '__main__':
    run()
