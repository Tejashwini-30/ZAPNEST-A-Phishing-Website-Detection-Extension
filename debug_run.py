"""
debug_run.py - quick tests for your running Flask app
Requires 'requests' installed: pip install requests
"""

import requests, json

BASE = "http://127.0.0.1:5000"

tests = [
    ("Legit (google)", "https://www.google.com"),
    ("Phish-synthetic", "http://www.bank-login.verify-account.com/secure-login")
]

print("== Quick debug tests ==")
for name, url in tests:
    print(f"\n-- Test: {name} --")
    r = requests.post(f"{BASE}/debug_predict", json={"url": url}, timeout=15)
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2))

# also test a dataset sample (index 0)
print("\n-- Test sample from CSV (idx=0) --")
r2 = requests.get(f"{BASE}/test_sample/0", timeout=15)
print("Status:", r2.status_code)
print(json.dumps(r2.json(), indent=2))
