#!/usr/bin/env python3
import requests
from requests.auth import HTTPDigestAuth

# Your phone details
PHONE_IP = "192.168.6.103"
USERNAME = "admin"
PASSWORD = "aikhanlabit"

# Test different API endpoints
endpoints = [
    "/",
    "/cgi-bin/api-get_call_status",
    "/api/v1/call/status",
    "/cgi-bin/api-get_status",
    "/cgi-bin/api-get_phone_info"
]

print("Testing connection to Grandstream phone...")
print(f"IP: {PHONE_IP}")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
print("-" * 50)

for endpoint in endpoints:
    try:
        url = f"http://{PHONE_IP}{endpoint}"
        print(f"Testing: {url}")
        
        response = requests.get(url, auth=HTTPDigestAuth(USERNAME, PASSWORD), timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # First 200 characters
        print("-" * 30)
        
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 30)
