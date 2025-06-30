def is_spam(message_text):
    reklama_sozlar = ["reklama", "https://", "@", "obuna", "kanalga qo‘shiling", "promo", "skidka"]
    for soz in reklama_sozlar:
        if soz in message_text.lower():
            return True
    return False

def handle_new_message(bot, message):
    # Agar foydalanuvchi admin bo‘lsa — hech nima qilmaydi
    try:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            return
    except Exception as e:
        print("Admin tekshiruvda xatolik:", e)
        return

    if is_spam(message.text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print("Xabarni o‘chirishda xatolik:", e)
