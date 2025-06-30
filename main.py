import os
import re
import time
import threading
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Reklama linklarini aniqlash uchun regex
LINK_REGEX = r"(https?://\S+|t\.me/\S+|telegram\.me/\S+)"

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return '✅ Bot ishlayapti!'

@bot.message_handler(content_types=['text'])
def delete_ads(message):
    if re.search(LINK_REGEX, message.text, re.IGNORECASE):
        try:
            # Adminlar ro'yxatini olamiz
            chat_admins = bot.get_chat_administrators(message.chat.id)
            admin_ids = [admin.user.id for admin in chat_admins]

            # Faqat oddiy foydalanuvchi reklama yuborsa
            if message.from_user.id not in admin_ids:
                bot.delete_message(message.chat.id, message.message_id)

                # Username yoki ism
                user = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

                # Ogohlantiruvchi xabar
                warning = bot.send_message(
                    message.chat.id,
                    f"⚠️ {user}, iltimos reklama tarqatmang!"
                )

                # 10 soniyada ogohlantirishni o'chirish uchun threading
                def delete_warning():
                    time.sleep(10)
                    try:
                        bot.delete_message(message.chat.id, warning.message_id)
                    except:
                        pass

                threading.Thread(target=delete_warning).start()

        except Exception as e:
            print(f"Xatolik: {e}")

# Webhook sozlash
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# Flask ishga tushurish
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
