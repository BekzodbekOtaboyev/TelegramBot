import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
import threading
import time
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

SPAM_KALITLAR = ["http", "https", "t.me", "@" , "sotib oling"]

def delete_after_delay(chat_id, message_id, delay=5):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print("Xatolik:", e)

@bot.message_handler(commands=['start'])
def start(message):
    bot_link = "https://t.me/Bek_qoravulbot?startgroup=true"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Botni guruhga qo‘shish", url=bot_link))
    bot.send_message(message.chat.id, "👋 Assalomu alaykum! Botni guruhga qo‘shib foydalaning:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def spam_filter(message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    try:
        adminlar = bot.get_chat_administrators(message.chat.id)
        foydalanuvchi_adminmi = any(admin.user.id == message.from_user.id for admin in adminlar)
        if foydalanuvchi_adminmi:
            return
    except Exception as e:
        print("Admin tekshiruvida xatolik:", e)

    matn = message.text.lower()
    if any(kalit in matn for kalit in SPAM_KALITLAR):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            msg1 = bot.send_message(message.chat.id, "❌ Reklama o‘chirildi.")
            threading.Thread(target=delete_after_delay, args=(msg1.chat.id, msg1.message_id)).start()
            username = message.from_user.username
            ogohlantirish = f"@{username}, iltimos reklama tarqatmang!" if username else "Iltimos reklama tarqatmang!"
            msg2 = bot.send_message(message.chat.id, ogohlantirish)
            threading.Thread(target=delete_after_delay, args=(msg2.chat.id, msg2.message_id)).start()
        except Exception as e:
            print("Xatolik:", e)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return '', 200
    return 'Bot ishlayapti!', 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()
print("Bot ishga tushdi.")
#bot.polling(none_stop=True)