import os
import time
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
from dotenv import load_dotenv

# .env fayldan tokenni olish
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

SPAM_KALITLAR = ["http", "https", "t.me", "telegram.me", "@"]

# ➖ Xabarni kechiktirib o‘chirish funksiyasi
def delete_after_delay(chat_id, message_id, delay=10):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print("Xatolik:", e)

# ✅ /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot_link = f"https://t.me/{bot.get_me().username}?startgroup=true"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Botni guruhga qo‘shish", url=bot_link))

    bot.send_message(
        message.chat.id,
        "🤖 *Assalomu alaykum!*\n\nReklama tozalovchi bot aktiv ishlamoqda.\n"
        "Uni guruhga qo‘shing va *admin* qiling!\n\n"
        "Agar bot ishlamay qolsa, *@uzbek_developer008* ga murojaat qiling!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

    # 🔔 Start bosgan foydalanuvchiga bitta umumiy xabar yuborish
    try:
        bot.send_message(
            message.chat.id,
            "📢 Bot administratori tomonidan xatoliklar to‘g‘irlandi.\n"
            "Noqulayliklar uchun uzr so‘raymiz!\n"
            "Botdan yana foydalanishingiz mumkin ✅"
        )
    except Exception as e:
        print("Bildirishnoma yuborishda xatolik:", e)

# 🚫 Reklama xabarlarini filtrlash
@bot.message_handler(content_types=['text'])
def spam_filter(message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    try:
        admins = bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]

        user_id = message.from_user.id
        is_admin = user_id in admin_ids
        is_bot = message.from_user.is_bot

        # Admin bo‘lmagan foydalanuvchi yoki admin bo‘lmagan bot
        if not is_admin and any(k in message.text.lower() for k in SPAM_KALITLAR):
            bot.delete_message(message.chat.id, message.message_id)

            # Faqat oddiy foydalanuvchi uchun ogohlantirish
            if not is_bot:
                user = (
                    f"@{message.from_user.username}"
                    if message.from_user.username
                    else message.from_user.first_name
                )

                warning = bot.send_message(
                    message.chat.id,
                    f"⚠️ {user}, iltimos reklama tarqatmang!"
                )
                threading.Thread(target=delete_after_delay, args=(warning.chat.id, warning.message_id)).start()

            # "Reklama o‘chirildi" xabari
            msg = bot.send_message(message.chat.id, "❌ Reklama o‘chirildi.")
            threading.Thread(target=delete_after_delay, args=(msg.chat.id, msg.message_id)).start()

    except Exception as e:
        print("Spam tekshiruvida xatolik:", e)

# 🌐 Flask - webhook
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return '', 200
    return '✅ Bot ishlayapti!', 200

# 🚀 Web serverni ishga tushurish
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()
print("Bot ishga tushdi.")
# bot.polling(none_stop=True)
