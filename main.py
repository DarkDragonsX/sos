import os
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from commander import reply  # ✅ مهم جداً لتفعيل reply.py

# ✅ توكن البوت
TOKEN = "7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM"
ADMIN_ID = 8196476936

# ✅ رسائل الترحيب
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

COMMANDER_FOLDER = "commander"
admin_custom_messages = []
user_custom_messages = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = random.choice(admin_custom_messages or admin_start_messages) if user_id == ADMIN_ID else random.choice(user_custom_messages or user_start_messages)
    await update.message.reply_text(msg)

async def run_scripts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("🚫 هذا الأمر خاص بالإدارة فقط.")
    result = ""
    for file in os.listdir(COMMANDER_FOLDER):
        if file.endswith(".py"):
            try:
                exec(open(os.path.join(COMMANDER_FOLDER, file)).read())
                result += f"✅ تم تنفيذ: {file}\n"
            except Exception as e:
                result += f"❌ خطأ في {file}: {e}\n"
    await update.message.reply_text(result)

async def add_admin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        msg = " ".join(context.args)
        if msg:
            admin_custom_messages.append(msg)
            await update.message.reply_text("✅ تمت إضافة رسالة تشغيل إدارية.")

async def clear_admin_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        admin_custom_messages.clear()
        await update.message.reply_text("🧹 تم حذف جميع رسائل التشغيل الإدارية.")

async def add_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        msg = " ".join(context.args)
        if msg:
            user_custom_messages.append(msg)
            await update.message.reply_text("✅ تمت إضافة رسالة تشغيل للمستخدم.")

async def clear_user_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        user_custom_messages.clear()
        await update.message.reply_text("🧹 تم حذف جميع رسائل المستخدم العادية.")

async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = [f for f in os.listdir(COMMANDER_FOLDER) if f.endswith(".py")]
    if files:
        await update.message.reply_text("📁 الملفات في commander:\n" + "\n".join(files))
    else:
        await update.message.reply_text("📂 لا توجد ملفات أوامر حالياً.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # أوامر البوت
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_scripts))
    app.add_handler(CommandHandler("addadminmsg", add_admin_msg))
    app.add_handler(CommandHandler("clearadminmsg", clear_admin_msgs))
    app.add_handler(CommandHandler("addusermsg", add_user_msg))
    app.add_handler(CommandHandler("clearusermsg", clear_user_msgs))
    app.add_handler(CommandHandler("listcmd", list_commands))

    # ✅ تفعيل أوامر reply.py
    reply.register_handlers(app)

    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
