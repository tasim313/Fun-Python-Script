import requests
from bs4 import BeautifulSoup
import re

host = "192.168.1.55"

# Get the main page
url = f"http://{host}"
print(f"Analyzing {url}")
print("="*60)

response = requests.get(url, timeout=10, verify=False)
print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
print(f"Content Length: {len(response.text)} bytes")
print(f"\nFirst 1000 characters of response:")
print(response.text[:1000])

# Look for redirects
if response.history:
    print(f"\nRedirected from: {response.history[0].url}")
    print(f"Redirected to: {response.url}")

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links
print("\n" + "="*60)
print("LINKS FOUND:")
print("="*60)
for link in soup.find_all('a', href=True):
    print(f"  {link.get('href')}")

# Find all forms
print("\n" + "="*60)
print("FORMS FOUND:")
print("="*60)
for form in soup.find_all('form'):
    print(f"  Action: {form.get('action')}")
    print(f"  Method: {form.get('method', 'GET')}")
    for input_field in form.find_all('input'):
        print(f"    Input: {input_field.get('name')} ({input_field.get('type', 'text')})")

# Find all scripts
print("\n" + "="*60)
print("SCRIPTS FOUND:")
print("="*60)
for script in soup.find_all('script', src=True):
    print(f"  {script.get('src')}")

# Try common paths
print("\n" + "="*60)
print("TESTING COMMON PATHS:")
print("="*60)

common_paths = [
    "/login",
    "/admin",
    "/index.html",
    "/index.php",
    "/cgi/login",
    "/api/login",
    "/webservice/login",
    "/pbx",
    "/web",
    "/sms",
    "/messages",
    "/cgi/API?action=login",
]

for path in common_paths:
    try:
        test_url = f"http://{host}{path}"
        resp = requests.get(test_url, timeout=3, verify=False)
        if resp.status_code == 200:
            print(f"  ✓ {path} - {resp.status_code} ({len(resp.text)} bytes)")
        elif resp.status_code in [301, 302, 303, 307, 308]:
            print(f"  → {path} - Redirect to {resp.headers.get('Location', 'unknown')}")
        else:
            print(f"  ✗ {path} - {resp.status_code}")
    except:
        print(f"  ✗ {path} - Error")