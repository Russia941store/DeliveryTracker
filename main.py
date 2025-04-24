# main.py
import asyncio
import logging
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

logging.basicConfig(level=logging.INFO)

async def main():
    print(">>> Инициализация приложения")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    print(f">>> Установка вебхука: {WEBHOOK_URL}")
    await app.bot.set_webhook(WEBHOOK_URL)
    print(">>> Запуск приложения через webhook...")
    await app.start()
    print(">>> Готово. Ждём события...")

if __name__ == "__main__":
    asyncio.run(main())