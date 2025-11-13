import os
import asyncio
from telegram.ext import ApplicationBuilder
from commander import register_commands
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

if not TOKEN:
    raise SystemExit("🚫 Missing TELEGRAM_TOKEN!")

async def main():
    # إنشاء التطبيق مباشرة بدون Updater
    app = ApplicationBuilder().token(TOKEN).build()
    
    # تسجيل الأوامر
    register_commands(app)

    print("✅ بوت السيد أيمن يعمل الآن (polling)...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
