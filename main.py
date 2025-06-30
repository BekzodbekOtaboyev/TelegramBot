import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return '✅ Bot ishlayapti!'

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"👋 Siz yubordingiz: {message.text}")

# Webhookni o‘rnatamiz
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
