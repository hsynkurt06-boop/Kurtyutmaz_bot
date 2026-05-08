import os
import asyncio
from telethon import TelegramClient, events

# Değişkenleri Railway'den çekiyoruz
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = int(os.environ.get("SOURCE_GROUP_ID"))
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# Sadece belirlediğimiz sinyal grubunu dinle
@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID)) 
async def handler(event):
    msg = event.message.message or ""
    msg_upper = msg.upper()
    
    # Sadece BTC ve ETH sinyallerini filtrele
    hedefler = ["ETHUSD", "BTCUSD"]
    
    if any(k in msg_upper for k in hedefler):
        try:
            # Sinyali senin şahsi botuna iletir
            await bot_client.send_message(MY_CHAT_ID, f"🎯 YENİ SİNYAL YAKALANDI!\n\n{msg}")
            print(f"Sinyal başarıyla iletildi: {msg[:30]}")
        except Exception as e:
            print(f"Gönderme hatası: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print(f"SİSTEM ÇALIŞIYOR: {SOURCE_GROUP_ID} grubunda BTC ve ETH takibi yapılıyor.")
    await user_client.run_until_disconnected()

asyncio.run(main())
