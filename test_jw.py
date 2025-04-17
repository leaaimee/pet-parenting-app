import requests



BASE_URL = "http://127.0.0.1:5000"  # Change if you're using a different port

# Step 1: Get JWT token
response = requests.post(f"{BASE_URL}/token", json={"username": "Ellen Ripley"})
print("🔑 Token response:", response.json())

# Step 2: Access protected route
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

protected = requests.get(f"{BASE_URL}/protected", headers=headers)
print("🛡️ Protected response (raw):", protected.text)
print("✅ Status Code:", protected.status_code)

