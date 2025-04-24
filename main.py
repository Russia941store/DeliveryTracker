# main.py
import asyncio
from telegram.ext import Application, ApplicationBuilder, CommandHandler
from handlers import start_handler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # берем токен из переменной окружения
WEBHOOK_PATH = f"/{BOT_TOKEN}"  # по этому пути Telegram будет отправлять сообщения
PORT = int(os.environ.get("PORT", 8443))  # стандартный порт
APP_URL = os.environ.get("WEBHOOK_URL")  # твой публичный адрес на Amvera

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))

    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=f"{APP_URL}{WEBHOOK_PATH}")  # Регистрируем webhook в Telegram
    await app.updater.start_webhook(
        listen="0.0.0.0",        # слушаем на всех интерфейсах
        port=PORT,              # порт (стандартный 8443)
        webhook_path=WEBHOOK_PATH,  # путь, куда прилетают сообщения от Telegram
    )
    await app.updater.wait_until_closed()  # ждем, пока не остановят

if __name__ == "__main__":
    asyncio.run(main())