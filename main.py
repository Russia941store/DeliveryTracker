# main.py

import asyncio
from config import BOT_TOKEN, WEBHOOK_URL
from telegram.ext import ApplicationBuilder

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # app.add_handler(...) ← Добавь нужные обработчики сюда
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    print("Бот запущен через вебхук...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())