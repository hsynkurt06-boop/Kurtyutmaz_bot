import os
import asyncio
from telethon import TelegramClient, events

# Değişkenleri Railway'den alıyoruz
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = int(os.environ.get("SOURCE_GROUP_ID"))
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# SADECE senin bulduğun ID'yi dinleyen özel fonksiyon
@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID))
async def handler(event):
    msg = event.message.message or ""
    
    # Filtre: Mesajda ETH geçiyorsa bota gönder
    if "ETH" in msg.upper():
        try:
            await bot_client.send_message(MY_CHAT_ID, f"🚨 YENİ ETH SİNYALİ:\n\n{msg}")
            print(f"Sinyal gönderildi: {msg[:20]}...")
        except Exception as e:
            print(f"Hata oluştu: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print(f"BOT AKTİF: Sadece {SOURCE_GROUP_ID} grubu dinleniyor...")
    await user_client.run_until_disconnected()

asyncio.run(main())
