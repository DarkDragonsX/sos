from bot import bot, ADMIN_ID
import json
import os

DATA_FILE = 'responses.json'

# تحميل البيانات
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# حفظ البيانات
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# حالات المستخدمين
user_states = {}  # user_id -> state
temp_data = {}    # user_id -> {'trigger': ..., 'responses': [...]}

# ========= أوامر =========

@bot.message_handler(func=lambda m: m.text == "اضف رد عشوائي")
def start_add_response(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    user_states[user_id] = 'awaiting_trigger'
    bot.reply_to(message, "📝 أرسل الكلمة أو الجملة التي تريدني أن أتعرف عليها 🔑")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'awaiting_trigger')
def receive_trigger(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    trigger = message.text.strip()
    temp_data[user_id] = {'trigger': trigger, 'responses': []}
    user_states[user_id] = 'awaiting_response'
    bot.reply_to(message, f"📌 تم حفظ الكلمة: [{trigger}]\n💬 أرسل الرد الآن، واكتب (احفظ) عندما تنتهي")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'awaiting_response')
def receive_response(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    text = message.text.strip()

    if text.lower() == "احفظ":
        trigger = temp_data[user_id]['trigger']
        responses = temp_data[user_id]['responses']
        data = load_data()
        if trigger not in data:
            data[trigger] = []
        data[trigger].extend(responses)
        save_data(data)
        user_states.pop(user_id)
        temp_data.pop(user_id)
        bot.reply_to(message, f"✅ تم حفظ {len(responses)} رد(ود) للكلمة [{trigger}] بنجاح 🎉")
    else:
        temp_data[user_id]['responses'].append(text)
        bot.reply_to(message, f"📥 تم إضافة رد مؤقت ✅\n🗨️ عدد الردود المؤقتة: {len(temp_data[user_id]['responses'])}")

@bot.message_handler(func=lambda m: m.text == "حذف رد")
def start_delete_response(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    user_states[user_id] = 'awaiting_delete'
    bot.reply_to(message, "🗑️ أرسل الكلمة أو الجملة التي تريد حذف ردها")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'awaiting_delete')
def delete_response(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    key = message.text.strip()
    data = load_data()
    if key in data:
        data.pop(key)
        save_data(data)
        bot.reply_to(message, f"🗑️ تم حذف جميع الردود المرتبطة بـ [{key}] بنجاح")
    else:
        bot.reply_to(message, f"⚠️ لا يوجد رد محفوظ بهذه الكلمة [{key}]")
    user_states.pop(user_id)

@bot.message_handler(func=lambda m: m.text == "عرض الردود")
def show_responses(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    data = load_data()
    if not data:
        bot.reply_to(message, "📭 لا توجد ردود محفوظة حالياً.")
        return

    reply = "📚 *الردود المحفوظة:*\n\n"
    for i, (trigger, responses) in enumerate(data.items(), 1):
        reply += f"{i}. 🔑 *{trigger}* → {len(responses)} رد\n"
    bot.reply_to(message, reply, parse_mode="Markdown")
