#main.py

import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from handlers import main_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("WEBHOOK_URL")  # Сюда ты уже подставил URL

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(main_handler)
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=f"{APP_URL}/webhook")
    print("Бот запущен через вебхук...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())