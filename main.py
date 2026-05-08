import os
from telethon import TelegramClient, events

# .env'den veya Railway environment variables'dan al
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOURCE_GROUP_ID = int(os.environ.get("SOURCE_GROUP_ID"))
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))

client = TelegramClient("session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_GROUP_ID))
async def handler(event):
    msg = event.message.message or ""
    if "ETH" in msg.upper():
        await client.send_message(MY_CHAT_ID, f"🚨 ETH SİNYALİ:\n\n{msg}")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot çalışıyor...")
    await client.run_until_disconnected()

import asyncio
asyncio.run(main())
