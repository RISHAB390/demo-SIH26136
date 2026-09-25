import urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:8001/static/uploads/3ddce0b59c994a3db56cd15a3647b190.png") as f:
        print("Download status:", f.status)
except Exception as e:
    print(e)
