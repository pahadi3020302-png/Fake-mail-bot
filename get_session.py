from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 36460415         # ← अपना REAL API_ID डालें
API_HASH = '37e0387f3d9c0bc7e0414e4a99a89db1'  # ← अपना REAL API_HASH डालें

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    client.start()
    session_str = client.session.save()
    print("✅ आपका String Session:\n")
    print(session_str)
