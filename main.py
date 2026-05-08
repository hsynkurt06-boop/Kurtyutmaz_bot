import os
import asyncio
from telethon import TelegramClient, events, functions

# --- DEĞİŞKENLER ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SOURCE_GROUP_ID = -1002539244253
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID"))
USERS_FILE = "users.txt"

# --- VERİTABANI İŞLEMLERİ ---
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

# --- CLİENT KURULUMLARI ---
user_client = TelegramClient("user_session", API_ID, API_HASH)
bot_client = TelegramClient("bot_session", API_ID, API_HASH)

# --- BOT PROFİLİNİ GÜNCELLEME (ABONE SAYISI) ---
async def update_bot_bio():
    try:
        users = get_users()
        count = len(users)
        # Botun 'Hakkında' kısmını günceller
        await bot_client(functions.account.UpdateProfileRequest(
            about=f"📊 Toplam {count} Aktif Abone | Otomatik Sinyal Botu"
        ))
        print(f"Bot bio güncellendi: {count} abone.")
    except Exception as e:
        print(f"Bio güncelleme hatası: {e}")

# --- KOMUTLAR ---

# /start: Yeni kullanıcı kaydı
@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.chat_id
    if add_user(user_id):
        await event.respond("✅ Bot aktif! Sadece BTCUSD ve ETHUSD sinyalleri size iletilecektir.")
        await update_bot_bio() # Sayı arttığı için bioyu güncelle
    else:
        await event.respond("Zaten sinyal listesindesiniz.")

# /kisi: Sadece admin kaç kişi olduğunu görür
@bot_client.on(events.NewMessage(pattern='/kisi'))
async def count_handler(event):
    if event.chat_id == MY_CHAT_ID:
        users = get_users()
        await event.respond(f"📈 Şu an toplam {len(users)} kişi abone.")
    else:
        await event.respond("Bu komut sadece yönetici içindir.")

# /duyuru [mesaj]: Admin tüm abonelere mesaj atar
@bot_client.on(events.NewMessage(pattern='/duyuru'))
async def broadcast_handler(event):
    if event.chat_id == MY_CHAT_ID:
        msg = event.message.message.replace('/duyuru', '').strip()
        if not msg:
            return await event.respond("Lütfen göndermek istediğiniz mesajı yazın. Örn: /duyuru Selam!")
        
        users = get_users()
        basarili = 0
        for user_id in users:
            try:
                await bot_client.send_message(int(user_id), f"📢 DUYURU:\n\n{msg}")
                basarili += 1
            except: pass
        await event.respond(f"✅ Duyuru {basarili} kişiye başarıyla iletildi.")

# --- SİNYAL YAKALAMA ---
@user_client.on(events.NewMessage(chats=SOURCE_GROUP_ID)) 
async def signal_handler(event):
    msg = event.message.message or ""
    msg_upper = msg.upper()
    
    if any(k in msg_upper for k in ["ETHUSD", "BTCUSD"]):
        users = get_users()
        for user_id in users:
            try:
                await bot_client.send_message(int(user_id), f"🎯 SİNYAL:\n\n{msg}")
            except:
                pass

# --- ANA ÇALIŞTIRMA ---
async def main():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.start()
    await update_bot_bio() # Açılışta bioyu güncelle
    print("SİSTEM AKTİF: Abone sayısı profil kısmına yansıtılıyor.")
    await user_client.run_until_disconnected()

asyncio.run(main())
