import requests
from bs4 import BeautifulSoup

host = "192.168.1.55"

# Start a session
session = requests.Session()

# Try to get the main page with different user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    "Yeastar/1.0",
]

for ua in user_agents:
    print(f"\nTrying User-Agent: {ua[:50]}...")
    headers = {'User-Agent': ua}
    
    try:
        response = session.get(f"http://{host}", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(f"  Status: 200")
            print(f"  Content length: {len(response.text)}")
            
            # Look for any meaningful content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for text content
            text = soup.get_text().strip()
            if text:
                print(f"  Text content preview: {text[:200]}")
            
            # Check for specific Yeastar patterns
            if "yeastar" in response.text.lower():
                print("  ✓ Found 'yeastar' in response")
            if "pbx" in response.text.lower():
                print("  ✓ Found 'pbx' in response")
            if "s系列" in response.text or "T系列" in response.text:
                print(f"  ✓ Found model info: {response.text[:200]}")
                
    except Exception as e:
        print(f"  Error: {e}")