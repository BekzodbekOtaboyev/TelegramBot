import re
from telebot.types import Message

# Reklama so‘zlari va havolalar
REKLAMA_KALITLARI = [
    "https://", "http://", "t.me/", "telegram.me/", "@",  # havolalar
    "obuna", "kanalga", "kanalimizga", "reklama", "follow", "subscribe"
]

def is_spam(text):
    text = text.lower()
    return any(kalit in text for kalit in REKLAMA_KALITLARI)

def handle_new_message(bot, message: Message):
    # Faqat oddiy foydalanuvchilardan kelgan xabarlarni tekshiramiz
    if message.chat.type in ['group', 'supergroup'] and not message.from_user.is_bot:
        if not message.from_user.id in get_admin_ids(bot, message.chat.id):
            if is_spam(message.text or ""):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    print(f"[INFO] Reklama o‘chirildi: {message.text}")
                except Exception as e:
                    print(f"[XATO] Xabarni o‘chirishda muammo: {e}")

def get_admin_ids(bot, chat_id):
    try:
        admins = bot.get_chat_administrators(chat_id)
        return [admin.user.id for admin in admins]
    except:
        return []
