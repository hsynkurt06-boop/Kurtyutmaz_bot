import os
import asyncio
from telethon import TelegramClient, events

# Değişkenler
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = -1002539244253
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))

# Kullanıcı listesini tutacak dosya adı
USERS_FILE = "users.txt"

# Dosya yoksa oluştur, varsa oku
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        f.write(str(MY_CHAT_ID) + "\n")

def get_users():
    with open(USERS_FILE, "r") as f:
        return {line.strip() for line in f if line.strip()}

def add_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")
        return True
    return False

user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# BOTU BAŞLATANLARI KAYDETME
@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.chat_id
    if add_user(user_id):
        await event.respond("Bot başarıyla başlatıldı! Sinyaller artık size de iletilecek.")
    else:
        await event.respond("Zaten sinyal listesindesiniz.")

# SİNYAL YAKALAMA VE HERKESE GÖNDERME
@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID)) 
async def signal_handler(event):
    msg = event.message.message or ""
    msg_upper = msg.upper()
    
    if any(k in msg_upper for k in ["ETHUSD", "BTCUSD"]):
        users = get_users()
        for user_id in users:
            try:
                await bot_client.send_message(int(user_id), f"🎯 YENİ SİNYAL:\n\n{msg}")
            except Exception as e:
                print(f"{user_id} gönderim hatası (Botu durdurmuş olabilir): {e}")

async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    print("OTOMATİK SİSTEM AKTİF: Start veren herkese sinyal gidecek.")
    await user_client.run_until_disconnected()

asyncio.run(main())
