#main.py
import asyncio
import logging
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        print(">>> Инициализация приложения")
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        register_handlers(app)
        await app.initialize()
        print(f">>> Установка вебхука: {WEBHOOK_URL}")
        await app.bot.set_webhook(WEBHOOK_URL)
        print(">>> Запуск приложения")
        await app.start()
        print(">>> Готово. Ждём события...")
        await app.updater.start_polling()  # добавим polling для живости, если webhook не работает
    except Exception as e:
        print(">>> Ошибка при запуске:", e)

if __name__ == "__main__":
    asyncio.run(main())