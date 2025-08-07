import json
import os
from telebot import TeleBot

API_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(API_TOKEN)

USERS_FILE = "users.json"

# Foydalanuvchini faylga yozish
def save_user(user_id):
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    save_user(user_id)
    bot.send_message(user_id, "👋 Salom! Botga xush kelibsiz.")

# Broadcasting funksiyasi
def send_broadcast_message():
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Hech qanday foydalanuvchi topilmadi.")
        return

    for user_id in users:
        try:
            bot.send_message(user_id,
                "📢 Bot administratori tomonidan xatoliklar to‘g‘irlandi.\n"
                "Noqulayliklar uchun uzr so‘raymiz!\n"
                "Botdan yana foydalanishingiz mumkin ✅"
            )
        except Exception as e:
            print(f"❌ Xatolik foydalanuvchi {user_id} ga yuborishda: {e}")

if __name__ == "__main__":
    send_broadcast_message()  # faqat 1 marta ishlaydi
