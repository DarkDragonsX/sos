ncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توكن البوت من متغير بيئي
TOKEN = os.getenv("7762777684:AAFngHPgagA7-IurRcOWf1ZjiW7OlpnSxfM")
ADMIN_ID = 8196476936

# رسائل بدء التشغيل
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

# مجلد السكربتات
COMMANDER_FOLDER = "commander"

# الرسائل المخصصة أثناء التشغيل
admin_custom_messages = []
user_custom_messages = []

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        msg = random.choice(admin_custom_messages or admin_start_messages)
    else:
        msg = random.choice(user_custom_messages or user_start_messages)
    await update.message.reply_text(msg)

# أمر لتشغيل كل سكربتات مجلد commander
async def run_scripts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("🚫 هذا الأمر خاص بالإدارة فقط.")

    result = ""
    for file in os.listdir(COMMANDER_FOLDER):
        if file.endswith(".py"):
            path = os.path.join(COMMANDER_FOLDER, file)
            try:
                exec(open(path).read())
                result += f"✅ تم تنفيذ: {file}\n"
            except Exception as e:
                result += f"❌ خطأ في {file}: {e}\n"
    await update.message.reply_text(result)

# إضافة رسالة تشغيل للإدارة
async def add_admin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = " ".join(context.args)
    if msg:
        admin_custom_messages.append(msg)
        await update.message.reply_text("✅ تمت إضافة رسالة تشغيل إدارية.")

# حذف رسائل الإدارة
async def clear_admin_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    admin_custom_messages.clear()
    await update.message.reply_text("🧹 تم حذف جميع رسائل التشغيل الإدارية.")

# إضافة رسالة تشغيل للمستخدم
async def add_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = " ".join(context.args)
    if msg:
        user_custom_messages.append(msg)
        await update.message.reply_text("✅ تمت إضافة رسالة تشغيل للمستخدم.")

# حذف رسائل المستخدم
async def clear_user_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    user_custom_messages.clear()
    await update.message.reply_text("🧹 تم حذف جميع رسائل المستخدم العادية.")

# عرض قائمة السكربتات
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = [f for f in os.listdir(COMMANDER_FOLDER) if f.endswith(".py")]
    if files:
        await update.message.reply_text("📁 الملفات في commander:\n" + "\n".join(files))
    else:
        await update.message.reply_text("📂 لا توجد ملفات أوامر حالياً.")

# الدالة الرئيسية
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_scripts))
    app.add_handler(CommandHandler("addadminmsg", add_admin_msg))
    app.add_handler(CommandHandler("clearadminmsg", clear_admin_msgs))
    app.add_handler(CommandHandler("addusermsg", add_user_msg))
    app.add_handler(CommandHandler("clearusermsg", clear_user_msgs))
    app.add_handler(CommandHandler("listcmd", list_commands))

    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
