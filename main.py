from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import re
import os

API_ID = int(os.environ.get('API_ID', 1234567))
API_HASH = os.environ.get('API_HASH', 'your_hash')
SESSION_STRING = os.environ.get('SESSION_STRING', None)
FAKE_MAIL_BOT = '@FakeMailBot'
STEP_DELAY = float(os.environ.get('STEP_DELAY', 1.5))

if SESSION_STRING:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    client = TelegramClient('my_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handle_email_list(event):
    if event.sender_id != (await client.get_me()).id:
        return
    text = event.raw_text.strip()
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@(?:hi2\.in|telegmail\.com)', text)
    if not emails:
        return
    emails = list(dict.fromkeys(emails))
    count = len(emails)
    if count > 100:
        await event.reply('⚠️ एक बार में 100 से ज्यादा न डालें।')
        return
    estimated = count * (STEP_DELAY * 2)
    await event.reply(f'⏳ कुल {count} ईमेल प्रोसेस हो रहे... करीब {int(estimated)} सेकंड लगेंगे।')
    for email in emails:
        await client.send_message(FAKE_MAIL_BOT, '/set')
        await asyncio.sleep(STEP_DELAY)
        await client.send_message(FAKE_MAIL_BOT, email)
        await asyncio.sleep(STEP_DELAY)
    await event.reply(f'✅ सभी {count} ईमेल तेज़ी से सेट कर दिए गए!')

@client.on(events.NewMessage(pattern='/setrange'))
async def set_range(event):
    if event.sender_id != (await client.get_me()).id:
        return
    parts = event.raw_text.split()
    if len(parts) != 5:
        await event.reply('❌ फॉर्मेट: /setrange user hi2.in 1 100')
        return
    _, prefix, domain, start_str, end_str = parts
    start, end = int(start_str), int(end_str)
    total = end - start + 1
    if total > 100:
        await event.reply('⚠️ एक बार में 100 से ज्यादा न डालें।')
        return
    await event.reply(f'⏳ {total} ईमेल प्रोसेस हो रहे...')
    for i in range(start, end + 1):
        email = f"{prefix}{i}@{domain}"
        await client.send_message(FAKE_MAIL_BOT, '/set')
        await asyncio.sleep(STEP_DELAY)
        await client.send_message(FAKE_MAIL_BOT, email)
        await asyncio.sleep(STEP_DELAY)
    await event.reply('✅ सभी भेज दिए गए!')

print("🚀 UserBot तेज़ मोड में चालू हो रहा है...")
client.start()
print("✅ अब 100 ईमेल की लिस्ट Saved Messages में डालें, सब तेज़ी से सेट होंगे!")
client.run_until_disconnected()
