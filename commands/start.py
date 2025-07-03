from bot import bot

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "مرحبا بك 🖐️، هذا أمر /start من ملف start.py")
