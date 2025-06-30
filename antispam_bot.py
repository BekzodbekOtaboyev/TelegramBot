from telebot import TeleBot, types

BAN_WORDS = ["https://", "http://", "t.me", "@", "#", "reklama", "reklam", "obuna", "ulanish", "kanalga"]
ADMINS = []  # admin user_id larini kiritsangiz bo'ladi

def is_spam(message: types.Message):
    text = message.text or ""
    for word in BAN_WORDS:
        if word.lower() in text.lower():
            return True
    return False

def handle_new_message(bot: TeleBot, message: types.Message):
    if is_spam(message):
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.send_message(chat_id=message.chat.id, text="❌ Reklama aniqlandi va o‘chirildi!", reply_to_message_id=message.message_id)
        except Exception as e:
            print("O‘chirishda xatolik:", e)
      