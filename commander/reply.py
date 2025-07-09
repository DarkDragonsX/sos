import json
import os
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

REPLIES_FILE = os.path.join("commander", "replies.json")
TEMP_STATE = {}
ADMIN_ID = 8196476936

def load_replies():
    if os.path.exists(REPLIES_FILE):
        with open(REPLIES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_replies(data):
    with open(REPLIES_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_admin(user_id):
    return user_id == ADMIN_ID

async def add_random_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return await update.message.reply_text("🚫 هذا الأمر مخصص للإدارة فقط.")

    TEMP_STATE[user_id] = {"step": "ask_keyword"}
    await update.message.reply_text("📝 أرسل الكلمة التي تريدني أن أرد عليها:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    if user_id not in TEMP_STATE:
        return

    state = TEMP_STATE[user_id]
    replies = load_replies()

    if state["step"] == "ask_keyword":
        state["keyword"] = message
        state["responses"] = []
        state["step"] = "collect_replies"
        await update.message.reply_text("💬 أرسل الردود الآن، وعندما تنتهي اكتب: احفظ")
        return

    elif state["step"] == "collect_replies":
        if message.lower() == "احفظ":
            keyword = state["keyword"]
            responses = state["responses"]
            if keyword in replies:
                replies[keyword].extend(responses)
            else:
                replies[keyword] = responses
            save_replies(replies)
            del TEMP_STATE[user_id]
            await update.message.reply_text(f"✅ تم حفظ {len(responses)} رد/ردود للكلمة: {keyword}")
        else:
            state["responses"].append(message)
            await update.message.reply_text("➕ تم حفظ الرد المؤقت... أرسل المزيد أو اكتب 'احفظ'")

async def show_reply_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return await update.message.reply_text("🚫 هذا الأمر مخصص للإدارة فقط.")

    replies = load_replies()
    if not replies:
        await update.message.reply_text("📭 لا توجد أي ردود محفوظة بعد.")
        return

    text = "📚 قائمة الردود المحفوظة:

"
    for word, resp_list in replies.items():
        text += f"🔹 *{word}*:
"
        for resp in resp_list:
            text += f"   - {resp}
"
        text += "\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def delete_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return await update.message.reply_text("🚫 هذا الأمر مخصص للإدارة فقط.")

    args = context.args
    if not args:
        await update.message.reply_text("❗ اكتب الكلمة التي تريد حذفها.
مثال: `/حذف_رد سلام`", parse_mode="Markdown")
        return

    keyword = " ".join(args)
    replies = load_replies()
    if keyword in replies:
        del replies[keyword]
        save_replies(replies)
        await update.message.reply_text(f"🗑️ تم حذف الردود المرتبطة بالكلمة: {keyword}")
    else:
        await update.message.reply_text("⚠️ لا توجد ردود محفوظة لهذه الكلمة.")

def register_handlers(app):
    app.add_handler(CommandHandler("اضف_رد_عشوائي", add_random_reply))
    app.add_handler(CommandHandler("عرض_القائمة", show_reply_list))
    app.add_handler(CommandHandler("حذف_رد", delete_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
