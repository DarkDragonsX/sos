from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(app, ADMIN_ID):
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = "💡 أوامر بوت السيد أيمن:\n"
        msg += "/start - تشغيل البوت\n"
        msg += "/add_reply - إضافة كلمات وردود جديدة (للأدمن فقط)\n"
        msg += "/delete_reply <الكلمة> - حذف كلمة مع ردودها (للأدمن فقط)\n"
        msg += "/save_words - لحفظ الكلمات بعد إدخالها\n"
        msg += "/save_replies - لحفظ الردود بعد إدخالها\n"
        await update.message.reply_text(msg)
    app.add_handler(CommandHandler("help", help_command))
