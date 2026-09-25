import urllib.request
import json
req = urllib.request.Request("http://127.0.0.1:8001/api/auth/login", method="POST", headers={"Content-Type": "application/json"})
data = json.dumps({"email": "contact@aquasense.io", "password": "demo123"}).encode()
try:
    with urllib.request.urlopen(req, data=data) as f:
        print("Login status:", f.status)
        print("Login response:", json.loads(f.read().decode()))
except urllib.error.HTTPError as e:
    print("Login status:", e.code)
    print("Login error:", e.read().decode())
except Exception as e:
    print(e)
