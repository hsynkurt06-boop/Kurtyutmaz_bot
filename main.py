import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
PHONE = os.environ.get("PHONE")
SOURCE_GROUP_ID = int(os.environ.get("SOURCE_GROUP_ID"))
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Kullanıcı hesabıyla giriş (grubu dinlemek için)
user_client = TelegramClient("user_session", API_ID, API_HASH)

# Bot ile mesaj göndermek için
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID))
async def handler(event):
    msg = event.message.message or ""
    if "ETH" in msg.upper():
        await bot_client.send_message(MY_CHAT_ID, f"🚨 ETH SİNYALİ:\n\n{msg}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start(phone=PHONE)
    print("Bot çalışıyor, grup dinleniyor...")
    await user_client.run_until_disconnected()

asyncio.run(main())
