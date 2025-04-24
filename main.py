# main.py
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes
)
from config import BOT_TOKEN
from handlers import (
    start, choose_manager, choose_delivery,
    write_comment, back_to_delivery,
    CHOOSE_MANAGER, CHOOSE_DELIVERY, WRITE_COMMENT
)

logging.basicConfig(level=logging.INFO)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 Получено сообщение!")
    await update.message.reply_text("Я получил: " + update.message.text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_MANAGER: [
                CallbackQueryHandler(choose_manager, pattern="^manager_")
            ],
            CHOOSE_DELIVERY: [
                CallbackQueryHandler(choose_delivery, pattern="^delivery_"),
                CallbackQueryHandler(choose_delivery, pattern="^back_to_manager$"),
                CallbackQueryHandler(back_to_delivery, pattern="^back_to_delivery$")
            ],
            WRITE_COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, write_comment),
                CallbackQueryHandler(back_to_delivery, pattern="^back_to_delivery$")
            ],
        },
        fallbacks=[],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # 👈 На случай простых текстов

    print("✅ Бот запущен. Ожидаем команды /start...")
    app.run_polling()

if __name__ == "__main__":
    main()