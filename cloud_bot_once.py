from instagrapi import Client
import os
import time
import random
import requests
from pathlib import Path

# Get from GitHub Secrets
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

print(f"Trying to login as: {IG_USERNAME}")

cl = Client()
cl.delay_range = [3, 8]  # Human delay

# IMPORTANT: Wait like a human before login
sleep_time = random.randint(25, 50)
print(f"Waiting {sleep_time}s like human to avoid block...")
time.sleep(sleep_time)

# LOGIN - with auto handling
try:
    # Try to login
    cl.login(IG_USERNAME, IG_PASSWORD)
    print("✅ Login SUCCESS!")

except Exception as e:
    print(f"❌ Login failed: {e}")
    print("Instagram blocked for now. Will try again in next run. Exiting clean.")
    # Exit with 0 so GitHub doesn't mark as spammy failure
    exit(0)

# === POST A MEME ===
try:
    print("Getting a meme...")
    
    # Download a random meme image
    meme_folder = Path("memes")
    meme_folder.mkdir(exist_ok=True)
    
    # Get random meme from API
    r = requests.get("https://meme-api.com/gimme/kenyamemes", timeout=20)
    if r.status_code != 200:
        r = requests.get("https://meme-api.com/gimme/memes", timeout=20)
    
    data = r.json()
    image_url = data.get("url")
    title = data.get("title", "Kenya meme 😂")[:80]

    if not image_url:
        print("No meme found, using fallback")
        image_url = "https://picsum.photos/1080/1080"

    # Download image
    img_data = requests.get(image_url, timeout=20).content
    image_path = meme_folder / "today.jpg"
    with open(image_path, "wb") as f:
        f.write(img_data)

    print(f"Posting: {title}")
    
    # Random Kenyan caption
    captions = [
        f"{title} 😂\n\n#kenya #kenyanmemes #nairobi #kisumu #mombasa #kenyantiktok #fyp",
        f"{title} 💀\n\nWakenya mtatunimaliza 😂 #kenya #memes #sirkal",
        f"{title} 😭😂\n\nTag a friend! #kenyamemes #kenya #funny"
    ]
    caption = random.choice(captions)

    # UPLOAD
    cl.photo_upload(
        path=str(image_path),
        caption=caption
    )
    print("✅ POSTED SUCCESSFULLY TO INSTAGRAM!")

except Exception as e:
    print(f"❌ Post failed: {e}")
    exit(0)

print("Done! Bot will post again in 6 hours.")
