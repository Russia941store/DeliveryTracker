# main.py
import asyncio
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

async def main():
    print(">>> Инициализация приложения")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    print(f">>> Установка вебхука: {WEBHOOK_URL}")
    await app.initialize()
    await app.bot.set_webhook(WEBHOOK_URL)
    print(">>> Запуск приложения через webhook...")
    await app.start()
    print(">>> Готово. Ждём события...")
    await app.updater.start()  # запуск цикла webhook listener
    await app.updater.wait_until_shutdown()  # блокирует выход из приложения

if __name__ == "__main__":
    asyncio.run(main())