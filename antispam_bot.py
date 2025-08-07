import telebot
from telebot import types
import time
import threading

TOKEN = "8124376102:AAGq9sk42u1s-QeBIJRm9E37bBlQQWhEJr4"
bot = telebot.TeleBot(TOKEN)

SPAM_KALITLAR = ["http", "https", "t.me", "@"]

def delete_after_delay(chat_id, message_id, delay=5):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Xatolik (o'chirishda): {e}")

@bot.message_handler(commands=['start'])
def start(message):
    bot_link = "https://t.me/Bek_qoravulbot?startgroup=true"
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("➕ Botni guruhga qo‘shish", url=bot_link)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum!\nBotdan foydalanishni boshlash uchun uni guruhga qo‘shing:",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def spam_filter(message):
    matn = message.text.lower()
    if any(kalit in matn for kalit in SPAM_KALITLAR):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            sent_msg = bot.send_message(message.chat.id, "❌ Reklama o‘chirildi.")
            # 5 soniyadan keyin reklama o'chirish haqidagi xabarni o'chirish uchun thread ishga tushuramiz
            threading.Thread(target=delete_after_delay, args=(sent_msg.chat.id, sent_msg.message_id)).start()

            username = message.from_user.username
            if username:
                text = f"@{username}, iltimos reklama tarqatmang!"
            else:
                text = "Iltimos, reklama tarqatmang!"

            bot.send_message(message.chat.id, text)

        except Exception as e:
            print(f"Xatolik: {e}")




bot.polling(none_stop=True, interval=0, timeout=60)

