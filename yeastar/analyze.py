import requests
from bs4 import BeautifulSoup
import re

host = "192.168.1.55"

# Get the page with a browser-like header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

response = requests.get(f"http://{host}", headers=headers, timeout=10)
print(f"Status: {response.status_code}")
print(f"Encoding: {response.encoding}")
print(f"\nFull HTML (first 2000 chars):")
print("="*60)
print(response.text[:2000])

# Parse with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all forms
print("\n" + "="*60)
print("FORMS FOUND:")
print("="*60)
for form in soup.find_all('form'):
    print(f"Action: {form.get('action')}")
    print(f"Method: {form.get('method', 'GET')}")
    print(f"Inputs:")
    for input_field in form.find_all('input'):
        print(f"  - {input_field.get('name')}: {input_field.get('type', 'text')}")

# Find all JavaScript files
print("\n" + "="*60)
print("JAVASCRIPT FILES:")
print("="*60)
for script in soup.find_all('script', src=True):
    print(f"  {script.get('src')}")

# Try to find the login endpoint
print("\n" + "="*60)
print("SEARCHING FOR LOGIN/API ENDPOINTS:")
print("="*60)

# Look for API calls in JavaScript
scripts = soup.find_all('script')
for script in scripts:
    if script.string:
        # Look for URLs in JavaScript
        urls = re.findall(r'["\'](/(?:api|cgi|webservice|login|ajax)[^"\']*?)["\']', script.string)
        for url in urls:
            print(f"  Found in JS: {url}")