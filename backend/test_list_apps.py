import urllib.request
import json
req = urllib.request.Request("http://127.0.0.1:8001/api/auth/login", method="POST", headers={"Content-Type": "application/json"})
data = json.dumps({"email": "rahul.verma@techboard.gov.in", "password": "demo123"}).encode()
try:
    with urllib.request.urlopen(req, data=data) as f:
        res = json.loads(f.read().decode())
        token = res["access_token"]
        print("Logged in as Evaluator")
        
    req2 = urllib.request.Request("http://127.0.0.1:8001/applications", method="GET", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req2) as f2:
        apps = json.loads(f2.read().decode())
        print("Applications:", json.dumps(apps, indent=2))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read().decode())
except Exception as e:
    print(e)
