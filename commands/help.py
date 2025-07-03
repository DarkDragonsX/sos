from bot import bot, ADMIN_ID
import json
import os

DATA_FILE = "custom_commands.json"

# تحميل أوامر محفوظة
def load_commands():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# حفظ الأوامر
def save_commands(commands):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(commands, f, ensure_ascii=False, indent=2)

# حالة المستخدم
user_states = {}  # user_id -> state

# ========= عرض الأوامر =========
@bot.message_handler(func=lambda m: m.text == "عرض الاوامر")
def show_commands(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    commands = load_commands()
    if not commands:
        bot.reply_to(message, "📭 لا توجد أوامر مضافة بعد.")
    else:
        reply = "📚 *قائمة الأوامر المضافة:*\n\n"
        for i, cmd in enumerate(commands, 1):
            reply += f"{i}. 🔸 {cmd}\n"
        bot.reply_to(message, reply, parse_mode="Markdown")

# ========= إضافة أمر =========
@bot.message_handler(func=lambda m: m.text == "اضف امر")
def start_add_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    user_states[user_id] = 'adding_command'
    bot.reply_to(message, "🆕 أرسل الأمر الجديد الذي تريد إضافته إلى القائمة:")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'adding_command')
def receive_new_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    new_cmd = message.text.strip()
    commands = load_commands()

    if new_cmd in commands:
        bot.reply_to(message, "⚠️ هذا الأمر مضاف مسبقاً.")
    else:
        commands.append(new_cmd)
        save_commands(commands)
        bot.reply_to(message, f"✅ تم إضافة الأمر: [{new_cmd}] بنجاح.")
    user_states.pop(user_id)

# ========= حذف أمر =========
@bot.message_handler(func=lambda m: m.text == "حذف امر")
def start_delete_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    commands = load_commands()
    user_id = message.from_user.id

    if not commands:
        bot.reply_to(message, "📭 لا توجد أوامر لحذفها.")
        return

    reply = "🗑️ *هذه قائمة الأوامر الحالية:*\n"
    for i, cmd in enumerate(commands, 1):
        reply += f"{i}. 🔸 {cmd}\n"
    reply += "\n✏️ أرسل الأمر الذي تريد حذفه:"
    user_states[user_id] = 'deleting_command'
    bot.reply_to(message, reply, parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'deleting_command')
def delete_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص للمطور فقط.")
        return

    user_id = message.from_user.id
    target = message.text.strip()
    commands = load_commands()

    if target in commands:
        commands.remove(target)
        save_commands(commands)
        bot.reply_to(message, f"🗑️ تم حذف الأمر: [{target}] بنجاح.")
    else:
        bot.reply_to(message, f"⚠️ لم يتم العثور على الأمر: [{target}] في القائمة.")
    user_states.pop(user_id)
