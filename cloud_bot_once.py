from instagrapi import Client
import os, time, random, requests
from pathlib import Path

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.delay_range = [5, 15]  # Very human

# Extra long human wait - 1 to 2 minutes
wait = random.randint(60, 120)
print(f"SAFE MODE: Waiting {wait}s...")
time.sleep(wait)

try:
    cl.login(IG_USERNAME, IG_PASSWORD)
    print("Login OK")
except Exception as e:
    print(f"Blocked, will retry tomorrow: {e}")
    exit(0)

try:
    # Only post 1 image per day - SAFE
    r = requests.get("https://meme-api.com/gimme/kenyamemes", timeout=20)
    if r.status_code != 200:
        r = requests.get("https://meme-api.com/gimme/memes", timeout=20)
    data = r.json()
    img_url = data.get("url", "https://picsum.photos/1080/1080")
    title = data.get("title", "Kenya")[:60]

    img_data = requests.get(img_url, timeout=20).content
    Path("memes").mkdir(exist_ok=True)
    p = Path("memes/today.jpg")
    p.write_bytes(img_data)

    caption = f"{title} 😂\n\n#kenya #kenyanmemes 🇰🇪"
    
    # Extra wait before posting - like human
    time.sleep(random.randint(15, 30))
    
    cl.photo_upload(str(p), caption)
    print("✅ POSTED SAFE!")
except Exception as e:
    print(f"Post fail: {e}")
    exit(0)
