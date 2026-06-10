import requests
import json

host = "192.168.1.55"
api_base = f"http://{host}/cgi"

# Common Yeastar API endpoints
endpoints = [
    f"{api_base}/API",
    f"{api_base}/sms",
    f"{api_base}/get_sms",
    f"http://{host}/api/sms",
    f"http://{host}/webservice/sms",
]

# Try common credentials
credentials = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "iyeastar"),
    ("support", "iyeastar"),
]

for endpoint in endpoints:
    print(f"\nTesting endpoint: {endpoint}")
    
    for username, password in credentials:
        try:
            # Try different authentication methods
            # Method 1: Basic auth
            response = requests.get(
                endpoint, 
                auth=(username, password),
                timeout=5,
                verify=False
            )
            
            if response.status_code == 200:
                print(f"  Success with {username}:{password}")
                print(f"  Response: {response.text[:200]}")
                
                # Try to parse JSON if present
                try:
                    data = response.json()
                    print(f"  JSON response: {json.dumps(data, indent=2)[:500]}")
                except:
                    pass
                    
            # Method 2: POST with form data
            login_data = {
                "username": username,
                "password": password,
                "action": "login"
            }
            response = requests.post(
                endpoint,
                data=login_data,
                timeout=5,
                verify=False
            )
            
            if response.status_code == 200 and "success" in response.text.lower():
                print(f"  POST login success with {username}:{password}")
                
        except Exception as e:
            pass

print("\n" + "="*60)
print("If web interface found, try accessing it manually:")
print(f"http://{host}")
print("Navigate to: Value-added Features -> SMS")