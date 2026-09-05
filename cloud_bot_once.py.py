import requests, os, random
from instagrapi import Client
IG_USERNAME = os.getenv("IG_USERNAME", "andrea984432")
IG_PASSWORD = os.getenv("IG_PASSWORD")
print("=== CLOUD BOT STARTING ===")
def get_meme():
    for sub in ["KenyanMemes","Kenya","nairobi","memes","dankmemes"]:
        try:
            r = requests.get(f"https://meme-api.com/gimme/{sub}", timeout=15).json()
            if r.get('url') and '.mp4' not in r['url']:
                return r['url'], r.get('title','')
        except:
            pass
    return None, None
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)
url, title = get_meme()
img = requests.get(url, timeout=15).content
open("temp.jpg","wb").write(img)
caption = f"{title[:120]}\n\nNimecheka 😂🇰🇪 #kenya #kenyanmemes"
cl.photo_upload("temp.jpg", caption=caption)
