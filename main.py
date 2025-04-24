# main.py
import os
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import ApplicationBuilder
from handlers import get_conv_handler
from config import BOT_TOKEN

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(get_conv_handler())
    print("Бот запущен...")
    await app.run_polling()

# === Правильный запуск в окружении Amvera ===
import asyncio

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass