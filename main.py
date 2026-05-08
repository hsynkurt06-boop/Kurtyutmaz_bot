import os
import asyncio
from telethon import TelegramClient, events

# Değişkenler
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# Takip etmek istediğin özel kelimeler listesi
HEDEF_KELIMELER = ["ETHUSD", "BTCUSD", "XAU USD"]

@user_client.on(events.NewMessage()) 
async def handler(event):
    msg = event.message.message or ""
    msg_upper = msg.upper()
    sender_id = event.chat_id
    
    # Mesajın içinde belirlediğimiz kelimelerden biri var mı kontrol et
    bulundu = any(kelime in msg_upper for kelime in HEDEF_KELIMELER)
    
    if bulundu:
        print(f"\n🎯 SİNYAL YAKALANDI!")
        print(f"📍 GRUP ID: {sender_id}")
        print(f"💬 MESAJ: {msg}")
        print(f"------------------------------\n")
        
        # Hem loglara yaz hem de kendi botuna raporla
        try:
            await bot_client.send_message(
                MY_CHAT_ID, 
                f"✅ DOĞRU GRUP TESPİT EDİLDİ!\n\n"
                f"📌 ID: `{sender_id}`\n"
                f"📝 Mesaj: {msg}"
            )
        except Exception as e:
            print(f"Bota mesaj gönderilirken hata: {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print("DEDEKTİF AKTİF: ETHUSD, BTCUSD ve XAU USD bekleniyor...")
    await user_client.run_until_disconnected()

asyncio.run(main())
