import os, re, random
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

learning_sessions = {}
responses = {}

os.makedirs("media/images", exist_ok=True)
os.makedirs("media/audio", exist_ok=True)

def register(app, ADMIN_ID):

    async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or update.effective_user.id != ADMIN_ID:
            return await update.message.reply_text("🚫 هذا الأمر للأدمن فقط!")
        learning_sessions[ADMIN_ID] = {"stage": "words", "words": [], "replies": []}
        await update.message.reply_text("🤖 أرسل الكلمات أولاً، ثم /save_words عند الانتهاء.")

    async def delete_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or update.effective_user.id != ADMIN_ID:
            return await update.message.reply_text("🚫 هذا الأمر للأدمن فقط!")
        if not context.args:
            return await update.message.reply_text("❌ استخدم: /delete_reply <الكلمة>")
        word = " ".join(context.args)
        if word in responses:
            del responses[word]
            await update.message.reply_text(f"🗑️ تم حذف '{word}' مع جميع الردود.")
        else:
            await update.message.reply_text("⚠️ هذه الكلمة غير موجودة.")

    async def save_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
        session = learning_sessions.get(ADMIN_ID)
        if not session or session["stage"] != "words":
            return await update.message.reply_text("لا توجد جلسة كلمات جارية.")
        if not session["words"]:
            return await update.message.reply_text("😅 لم ترسل أي كلمة بعد!")
        session["stage"] = "replies"
        await update.message.reply_text("✅ الكلمات محفوظة. الآن أرسل الردود (نص، صورة، صوت) ثم /save_replies")

    async def save_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
        session = learning_sessions.get(ADMIN_ID)
        if not session or session["stage"] != "replies":
            return await update.message.reply_text("لا توجد جلسة ردود جارية.")
        for word in session["words"]:
            responses[word] = session["replies"] if session["replies"] else [{"type":"text","content":"..."}]
        del learning_sessions[ADMIN_ID]
        await update.message.reply_text("🎉 تم الحفظ بنجاح سيدي ❤😊")

    async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
        user_id = update.effective_user.id
        text = update.message.text.strip() if update.message.text else None

        if user_id == ADMIN_ID and user_id in learning_sessions:
            session = learning_sessions[user_id]
            stage = session["stage"]
            if stage == "words" and text:
                session["words"].append(text)
                await update.message.reply_text("تم إضافة الكلمة ✅")
            elif stage == "replies":
                if text:
                    session["replies"].append({"type":"text","content":text})
                    await update.message.reply_text("تم إضافة الرد النصي ✅")
                elif update.message.photo:
                    file_id = update.message.photo[-1].file_id
                    session["replies"].append({"type":"photo","content":file_id})
                    await update.message.reply_text("تم إضافة صورة ✅")
                elif update.message.voice:
                    file_id = update.message.voice.file_id
                    session["replies"].append({"type":"voice","content":file_id})
                    await update.message.reply_text("تم إضافة ملف صوتي ✅")
                elif update.message.audio:
                    file_id = update.message.audio.file_id
                    session["replies"].append({"type":"audio","content":file_id})
                    await update.message.reply_text("تم إضافة ملف صوتي (audio) ✅")
        else:
            # Normal users: match and reply
            if not update.message.text:
                return
            replied = set()
            for word, reply_list in responses.items():
                matched = re.search(rf"(?<!\w){re.escape(word)}(?!\w)", update.message.text, re.IGNORECASE)
                if matched and word not in replied:
                    reply = random.choice(reply_list)
                    t = reply.get("type")
                    if t == "text":
                        await update.message.reply_text(reply["content"])
                    elif t == "photo":
                        await update.message.reply_photo(reply["content"])
                    elif t == "voice":
                        await update.message.reply_voice(reply["content"])
                    elif t == "audio":
                        await update.message.reply_audio(reply["content"])
                    replied.add(word)

    app.add_handler(CommandHandler("add_reply", add_reply))
    app.add_handler(CommandHandler("delete_reply", delete_reply))
    app.add_handler(CommandHandler("save_words", save_words))
    app.add_handler(CommandHandler("save_replies", save_replies))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, message_handler))
