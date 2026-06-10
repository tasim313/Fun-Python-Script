import requests

host = "192.168.1.55"

# Try to access the SMS page directly
sms_paths = [
    "/cgi/API",
    "/cgi/API?action=getSMS",
    "/cgi/API?action=getSMS&type=outbox",
    "/cgi/API?action=login",
    "/index.php?mod=sms",
    "/admin/index.php?mod=sms",
    "/pbx/index.php?mod=sms",
    "/webservice/sms.php",
    "/api/sms.php",
]

print("Trying SMS access paths:")
print("="*60)

for path in sms_paths:
    url = f"http://{host}{path}"
    try:
        response = requests.get(url, timeout=5, verify=False)
        if response.status_code == 200:
            print(f"\n✓ {path} - SUCCESS")
            print(f"  Response preview: {response.text[:300]}")
            
            # Try to see if it's a login page
            if 'login' in response.text.lower() or 'username' in response.text.lower():
                print("  → This appears to be a login page")
                
                # Try to login with default credentials
                login_data = {
                    'username': 'admin',
                    'password': 'admin',
                    'action': 'login'
                }
                
                login_response = requests.post(url, data=login_data, verify=False)
                if login_response.status_code == 200:
                    print(f"  → Login attempt response: {login_response.text[:200]}")
                    
        elif response.status_code in [301, 302]:
            print(f"→ {path} - Redirect to {response.headers.get('Location', 'unknown')}")
        else:
            print(f"✗ {path} - {response.status_code}")
    except Exception as e:
        print(f"✗ {path} - Error: {str(e)[:50]}")