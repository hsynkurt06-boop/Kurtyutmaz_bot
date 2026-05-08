import os
import asyncio
from telethon import TelegramClient, events

# Değişkenleri Railway'den alıyoruz
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = int(os.environ.get("SOURCE_GROUP_ID"))
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Session dosyası ile giriş yapıyoruz
user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID))
async def handler(event):
    msg = event.message.message or ""
    # Sadece ETHUSD içeren mesajları filtrele
    if "ETHUSD" in msg.upper():
        await bot_client.send_message(MY_CHAT_ID, f"🚨 YENİ ETHUSD SİNYALİ:\n\n{msg}")

async def main():
    # Bot ve Kullanıcı hesaplarını başlat
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start() 
    print("Sistem Aktif: ETHUSD sinyalleri bekleniyor...")
    await user_client.run_until_disconnected()

asyncio.run(main())
