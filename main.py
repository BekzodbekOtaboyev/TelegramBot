import os
import re
import time
import threading
from flask import Flask, request
import telebot
from telebot import types
from dotenv import load_dotenv

# .env fayldan token va webhook URL o'qiladi
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Reklama linklarini aniqlash uchun regex
LINK_REGEX = r"(https?://\S+|t\.me/\S+|telegram\.me/\S+)"

# Webhook qabul qilish
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/', methods=['GET'])
def index():
    return '✅ Bot ishlayapti!'

# /start komandasi uchun javob
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Tugma yaratish
    button = types.InlineKeyboardButton(
        text="➕ Guruhga qo‘shish",
        url=f"https://t.me/{bot.get_me().username}?startgroup=true"
    )
    markup = types.InlineKeyboardMarkup().add(button)

    # Xabar yuborish
    bot.send_message(
        chat_id,
    "🤖 *Assalamu alaykum!*\n\n"
    "Reklama tozalovchi bot aktiv ishlamoqda.📈✅\n"
    "Uni guruhga qo‘shing va *admin* qiling!\n\n"
    "Agar botda nozoliklar bo'lsa, *@uzbek_developer008* ga murojaat qiling!",
    reply_markup=markup,
    parse_mode='Markdown'
    )

# Reklama aniqlash va o'chirish
@bot.message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def delete_ads(message):
    try:
        # Agar anonim yoki noma'lum foydalanuvchi bo‘lsa — tashlab ketamiz
        if not message.from_user:
            return

        # Guruhdagi adminlarni olish
        admins = bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]

        user_id = message.from_user.id
        is_admin = user_id in admin_ids

        # LINK bo‘lsa va foydalanuvchi admin bo‘lmasa
        if not is_admin and re.search(LINK_REGEX, message.text, re.IGNORECASE):
            bot.delete_message(message.chat.id, message.message_id)

            # Faqat oddiy foydalanuvchiga ogohlantirish yuboriladi
            if not message.from_user.is_bot:
                user = (
                    f"@{message.from_user.username}"
                    if message.from_user.username
                    else message.from_user.first_name
                )

                warning = bot.send_message(
                    message.chat.id,
                    f"⚠️ {user}, iltimos reklama tarqatmang!"
                )

                def delete_warning():
                    time.sleep(10)
                    try:
                        bot.delete_message(message.chat.id, warning.message_id)
                    except:
                        pass

                threading.Thread(target=delete_warning).start()

    except Exception as e:
        print(f"Xatolik: {e}")



# Webhook sozlash va serverni ishga tushirish
if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
