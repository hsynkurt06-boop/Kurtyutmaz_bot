import os
import asyncio
from telethon import TelegramClient, events

# Değişkenleri Railway'den çekiyoruz
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# DİKKAT: 'chats' filtresini kaldırdım, böylece her şeyi duyacak
@user_client.on(events.NewMessage()) 
async def handler(event):
    msg = event.message.message or ""
    sender_id = event.chat_id
    
    # Bu satır Railway Loglarında "Gelen ID: -100xxxx" şeklinde görünecek
    print(f"--- YENİ MESAJ ---")
    print(f"Gelen ID: {sender_id}")
    print(f"Mesaj İçeriği: {msg}")
    print(f"------------------")
    
    # Eğer gelen mesajda ETH varsa yine de bota göndermeye çalışsın
    if "ETH" in msg.upper():
        try:
            await bot_client.send_message(MY_CHAT_ID, f"🚨 YAKALANAN SİNYAL:\n\n{msg}")
        except Exception as e:
            print(f"Mesaj gönderme hatası: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print("BOT TAM YETKİYLE AKTİF - TÜM GRUPLAR DİNLENİYOR...")
    await user_client.run_until_disconnected()

asyncio.run(main())
