import urllib.request
import json
import os
import requests

with open("test.pdf", "wb") as f:
    f.write(b"%PDF-1.4 test")
    
req = urllib.request.Request("http://127.0.0.1:8001/api/auth/login", method="POST", headers={"Content-Type": "application/json"})
data = json.dumps({"email": "contact@aquasense.io", "password": "demo123"}).encode()
try:
    with urllib.request.urlopen(req, data=data) as f:
        res = json.loads(f.read().decode())
        token = res["access_token"]
        print("Logged in as Startup")
        
    r = requests.post("http://127.0.0.1:8001/api/uploads", headers={"Authorization": f"Bearer {token}"}, files={"file": ("test.pdf", open("test.pdf", "rb"), "application/pdf")})
    print("Upload status:", r.status_code)
    print("Upload response:", r.text)
except Exception as e:
    print(e)
