import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

responses = {}
learning_sessions = {}

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 هذا الأمر للأدمن فقط!")
        return
    learning_sessions[ADMIN_ID] = {"stage": "words", "words": [], "replies": []}
    await update.message.reply_text("أرسل الكلمات للرد عليها. اكتب 'save' عند الانتهاء.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id == ADMIN_ID and user_id in learning_sessions:
        session = learning_sessions[user_id]
        stage = session["stage"]

        if stage == "words":
            if text.lower() == "save":
                session["stage"] = "replies"
                await update.message.reply_text("الآن أرسل الردود للرد على الكلمات. اكتب 'save' عند الانتهاء.")
            else:
                session["words"].append(text)
                await update.message.reply_text("تم إضافة الكلمة ✅")
        elif stage == "replies":
            if text.lower() == "save":
                for word in session["words"]:
                    responses[word] = session["replies"] if session["replies"] else ["..."]
                del learning_sessions[user_id]
                await update.message.reply_text("🎉 تم حفظ الردود بنجاح!")
            else:
                session["replies"].append(text)
                await update.message.reply_text("تم إضافة الرد ✅")
    else:
        for word, reply_list in responses.items():
            if word in text:
                await update.message.reply_text(reply_list[0])
                break

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("add_reply", add_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("✅ البوت يعمل الآن (polling)...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
