# main.py
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from telegram.ext import ApplicationBuilder
from handlers import get_conv_handler
from config import BOT_TOKEN

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(get_conv_handler())
    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())