import os
import asyncio
from telethon import TelegramClient, events

# Değişkenleri Railway'den alıyoruz
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = -1002539244253 # Sabitlendi, Railway'den çekmeye gerek kalmadı
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# SADECE hedef grubu dinle (Sonsuz döngüyü bu satır engeller)
@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID)) 
async def handler(event):
    msg = event.message.message or ""
    msg_upper = msg.upper()
    
    # Sadece bu iki kelimeyi ara
    hedefler = ["ETHUSD", "BTCUSD"]
    
    if any(k in msg_upper for k in hedefler):
        try:
            # Sinyali sana gönderir
            await bot_client.send_message(MY_CHAT_ID, f"🎯 SİNYAL:\n\n{msg}")
            print(f"Sinyal iletildi: {msg[:20]}")
        except Exception as e:
            print(f"Hata: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print("SİSTEM SABİTLENDİ: Sadece BTC ve ETH takibi yapılıyor.")
    await user_client.run_until_disconnected()

asyncio.run(main())
