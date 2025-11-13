from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(app, ADMIN_ID):
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👑 بوت السيد أيمن جاهز للعمل! 🚀")
    app.add_handler(CommandHandler("start", start))
