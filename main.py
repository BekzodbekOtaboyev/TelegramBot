import json
import os
from telebot import TeleBot

# Tokenni olish
API_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(API_TOKEN)

# Foydalanuvchilar fayli
USERS_FILE = "users.json"

# Har bir foydalanuvchining ID sini saqlash
def save_user(user_id):
    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as file:
            json.dump(users, file)

# /start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    save_user(user_id)

    bot.send_message(user_id, "👋 Salom! Botimizga xush kelibsiz.")

# Barcha foydalanuvchilarga bir martalik habar yuborish
def send_broadcast():
    with open("users.txt", "r") as file:
        users = set(file.read().splitlines())  # set orqali dublikat yo'qoladi
    for user_id in users:
        try:
            bot.send_message(user_id, "📢 Bot administratori tomonidan xatoliklar to‘g‘irlandi.\n"
                                      "Noqulayliklar uchun uzr so‘raymiz!\n"
                                      "Botdan yana foydalanishingiz mumkin ✅")
        except Exception as e:
            print(f"Xatolik: {e}")

    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for user_id in users:
        try:
            bot.send_message(user_id,
                "📢 Bot administratori tomonidan xatoliklar to‘g‘irlandi.\n"
                "Noqulayliklar uchun uzr so‘raymiz!\n"
                "Botdan yana foydalanishingiz mumkin ✅"
            )
        except Exception as e:
            print(f"Xatolik foydalanuvchi {user_id} ga yuborishda: {e}")

# Faqat sizcha: dastur ishga tushganda bu xabar yuboriladi
if __name__ == "__main__":
    send_broadcast()  # Bu faqat 1 marta ishga tushganda yuboradi
    bot.polling()
