# main.py
import asyncio
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    await app.initialize()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.start()
    print("Бот запущен через вебхук...")

    # Поддерживаем бот живым
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())