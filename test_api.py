import requests

try:
    resp = requests.post("http://127.0.0.1:8000/api/generate-logo", json={"prompt": "قطة", "remove_background": True})
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Success! Image data starts with: {data.get('image_data', '')[:50]}")
    else:
        print(f"Error Response: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
