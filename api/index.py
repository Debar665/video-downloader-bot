from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def send_video(chat_id, video_url):
    requests.post(f"{TELEGRAM_API}/sendVideo", json={
        "chat_id": chat_id,
        "video": video_url,
        "supports_streaming": True
    })

def get_tiktok_video(url):
    r = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
    if r.get("code") == 0:
        return r["data"]["play"]
    return None

@app.post("/api/index")
async def webhook(req: Request):
    data = await req.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return {"ok": True}

    if text.startswith("/start"):
        send_message(chat_id, "👋 Send me a TikTok or Instagram link!")
        return {"ok": True}

    if "tiktok.com" in text:
        send_message(chat_id, "⏳ Downloading...")
        video_url = get_tiktok_video(text)
        if video_url:
            send_video(chat_id, video_url)
        else:
            send_message(chat_id, "❌ Failed. Try another link.")
    elif "instagram.com" in text:
        send_message(chat_id, "⚠️ Instagram coming soon!")
    else:
        send_message(chat_id, "⚠️ Send a valid TikTok or Instagram link.")

    return {"ok": True}
