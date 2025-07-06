import telebot
import os
import random
import importlib.util
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN", "ضع_توكن_البوت_هنا")
ADMIN_USERNAME = "darkdragonsx"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app.onrender.com")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MESSAGES_FILE = 'startup_messages.txt'
editing_users = {}
new_messages = {}

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'w') as f:
            f.write("☺️ مرحباً أنا مريم بوت السيد darkdragonsx\nمبرمج تطبيقات ويب وأدوات كالي لينكس ❤\n")
    with open(MESSAGES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_messages(msgs):
    with open(MESSAGES_FILE, 'w') as f:
        for msg in msgs:
            f.write(msg + '\n')

@bot.message_handler(commands=['start'])
def handle_start(message):
    messages = load_messages()
    bot.send_message(message.chat.id, random.choice(messages))

@bot.message_handler(func=lambda msg: msg.text == 'تعديل رسالة تشغيل')
def handle_edit_command(message):
    if message.from_user.username != ADMIN_USERNAME:
        return bot.send_message(message.chat.id, "❌ هذا الأمر مخصص للأدمن فقط.")
    editing_users[message.chat.id] = True
    new_messages[message.chat.id] = []
    bot.send_message(message.chat.id, "📝 أرسل رسائل التشغيل واحدة تلو الأخرى.\n🖋️ عند الانتهاء، أرسل: احفظ")

@bot.message_handler(func=lambda msg: editing_users.get(msg.chat.id, False))
def handle_new_messages(message):
    text = message.text.strip()
    chat_id = message.chat.id
    if text.lower() == 'احفظ':
        msgs = new_messages.get(chat_id, [])
        if msgs:
            save_messages(msgs)
            bot.send_message(chat_id, f"✅ تم حفظ {len(msgs)} رسالة تشغيل جديدة.")
        else:
            bot.send_message(chat_id, "⚠️ لم يتم إرسال أي رسائل.")
        editing_users.pop(chat_id, None)
        new_messages.pop(chat_id, None)
    else:
        new_messages[chat_id].append(text)
        bot.send_message(chat_id, f"✅ تم حفظ: {text}")

def load_commands():
    commands_dir = './commands'
    if not os.path.exists(commands_dir):
        os.makedirs(commands_dir)
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            filepath = os.path.join(commands_dir, filename)
            spec = importlib.util.spec_from_file_location("command_module", filepath)
            command_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(command_module)
            if hasattr(command_module, 'register'):
                command_module.register(bot)

# Flask endpoint for webhook
@app.route("/", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK"

# إعداد البوت عند التشغيل على Render
@app.before_first_request
def setup():
    bot.remove_webhook()
    bot.set_webhook(WEBHOOK_URL)

load_commands()
