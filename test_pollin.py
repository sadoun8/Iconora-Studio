import requests
from urllib.parse import quote

english_prompt = "applying the accounting statement for stores and professional sales of electrical appliances, computers, etc"
filtered_prompt = english_prompt.replace("Design a logo for", "").replace("design a logo for", "").strip()
ai_prompt = f"minimalist professional flat vector icon of [{filtered_prompt}], purely symbolic graphic, NO TEXT, textless, NO LETTERS, no typography, white background, clean lines, flat design masterpiece, isolated"

url = f"https://image.pollinations.ai/prompt/{quote(ai_prompt)}?width=512&height=512&nologo=true"
print(url)
response = requests.get(url, timeout=120)

print(f"Status: {response.status_code}")
if response.status_code != 200:
    print(response.text)
