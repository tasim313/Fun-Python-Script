import requests
import re
from bs4 import BeautifulSoup

host = "192.168.1.55"

# Try common web ports
ports = [80, 443, 8080, 8088, 8443]

for port in ports:
    try:
        url = f"http://{host}:{port}"
        print(f"\nTrying {url}")
        
        response = requests.get(url, timeout=5, verify=False)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Found web interface on port {port}")
            print(f"Title: {re.findall('<title>(.*?)</title>', response.text, re.IGNORECASE)}")
            
            # Look for SMS in the page
            if 'sms' in response.text.lower():
                print("SMS-related content found!")
            
            # Try to find API endpoints
            api_patterns = ['api', 'cgi', 'webservice', 'rest']
            for pattern in api_patterns:
                if pattern in response.text.lower():
                    print(f"Found potential API endpoint: {pattern}")
                    
    except Exception as e:
        pass

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)