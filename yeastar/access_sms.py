from playwright.sync_api import sync_playwright
import json

def capture_sms_network_requests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Array to store captured requests
        captured_requests = []
        
        # Listen to all responses
        def on_response(response):
            url = response.url
            if 'WebCGI' in url or 'sms' in url.lower() or 'outbox' in url.lower():
                try:
                    body = response.text()
                    captured_requests.append({
                        'url': url,
                        'status': response.status,
                        'body': body[:1000]  # First 1000 chars
                    })
                    print(f"\n✓ Captured: {url}")
                    print(f"  Status: {response.status}")
                    print(f"  Body preview: {body[:200]}")
                except:
                    pass
        
        page.on('response', on_response)
        
        # Navigate and login
        print("Navigating to login page...")
        page.goto('http://192.168.1.55')
        
        # Fill login form
        page.fill('#username', 'admin')
        page.fill('#secret', 'aikhanlab')
        
        # Click login
        print("Logging in...")
        page.click('#btn-login')
        
        # Wait for login to complete
        page.wait_for_timeout(3000)
        
        # Now navigate to SMS section - you mentioned outbox has data
        print("\nLooking for SMS/Outbox section...")
        
        # Try to find and click SMS menu
        sms_selectors = [
            "a:has-text('SMS')",
            "a:has-text('Outbox')",
            "a:has-text('Message')",
            "text=SMS",
            "text=Outbox",
        ]
        
        for selector in sms_selectors:
            if page.locator(selector).count() > 0:
                print(f"Clicking: {selector}")
                page.click(selector)
                page.wait_for_timeout(3000)
                break
        
        # Take screenshot of current page
        page.screenshot(path="current_page.png")
        print("\nScreenshot saved as current_page.png")
        
        # Get page HTML
        html = page.content()
        with open("current_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Page HTML saved to current_page.html")
        
        # Wait for user to manually explore
        input("\nPress Enter after you've navigated to the outbox and seen the SMS data...")
        
        # Save all captured requests
        with open("captured_requests.json", "w") as f:
            json.dump(captured_requests, f, indent=2)
        
        print(f"\nCaptured {len(captured_requests)} requests")
        
        # Close browser
        browser.close()

# Run the capture
capture_sms_network_requests()