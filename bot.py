import telebot
import os
import runpy
from flask import Flask, request

# ✅ التوكن
TOKEN = '7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM'
bot = telebot.TeleBot(TOKEN)

# ✅ معرف المطور الأساسي
ADMIN_ID = 8196476936  # 👑 سيدي أيمن المحترم فقط

# ✅ إعداد Flask
app = Flask(__name__)
APP_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

# ✅ تشغيل كل ملفات commands/*.py
def run_all_commands():
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for file in os.listdir(commands_dir):
        if file.endswith('.py'):
            path = os.path.join(commands_dir, file)
            runpy.run_path(path)

# ✅ استقبال التحديثات من Webhook
@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# ✅ صفحة رئيسية للتأكد من تشغيل البوت
@app.route('/')
def home():
    return "✅ البوت يعمل بنجاح"

# ✅ إعداد Webhook
bot.remove_webhook()
bot.set_webhook(url=APP_URL)

# ✅ تشغيل جميع ملفات commands
run_all_commands()

# ✅ تشغيل تطبيق Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
