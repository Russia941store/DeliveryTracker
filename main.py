#main.py
import asyncio
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(WEBHOOK_URL)
    print("Бот запущен через вебхук...")
    await app.updater.start_polling()  # может быть убран, если не нужен

if __name__ == "__main__":
    asyncio.run(main())