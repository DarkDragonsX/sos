import os
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from commander import reply

TOKEN = "7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM"
ADMIN_ID = 8196476936

admin_start_messages = [
    "🤖 تم تشغيل بوت السيد أيمن العظيم 🔥👑",
    "⚡ بوت النخبة شغّال الآن، حيّاكم الله!",
    "🚀 البوت تحت قيادة فخامته السيد أيمن!"
]

user_start_messages = [
    "مرحباً! أنا بوت السيد أيمن 👋",
    "أهلاً بك في خدمة البوت، كيف يمكنني مساعدتك؟",
    "بوت الدفاع الإلكتروني هنا في الخدمة! 💻🛡️"
]

admin_custom_messages = []
user_custom_messages = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        msg = random.choice(admin_custom_messages or admin_start_messages)
    else:
        msg = random.choice(user_custom_messages or user_start_messages)
    await update.message.reply_text(msg)

async def add_admin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = " ".join(context.args)
    if msg:
        admin_custom_messages.append(msg)
        await update.message.reply_text("✅ تمت إضافة رسالة تشغيل إدارية.")

async def clear_admin_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    admin_custom_messages.clear()
    await update.message.reply_text("🧹 تم حذف جميع رسائل التشغيل الإدارية.")

async def add_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = " ".join(context.args)
    if msg:
        user_custom_messages.append(msg)
        await update.message.reply_text("✅ تمت إضافة رسالة تشغيل للمستخدم.")

async def clear_user_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    user_custom_messages.clear()
    await update.message.reply_text("🧹 تم حذف جميع رسائل المستخدم العادية.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addadminmsg", add_admin_msg))
    app.add_handler(CommandHandler("clearadminmsg", clear_admin_msgs))
    app.add_handler(CommandHandler("addusermsg", add_user_msg))
    app.add_handler(CommandHandler("clearusermsg", clear_user_msgs))

    reply.register_handlers(app)

    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
