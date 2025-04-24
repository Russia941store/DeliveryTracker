# handlers.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, CommandHandler, filters
from config import CHANNEL_ID
from keyboards import manager_keyboard, delivery_keyboard_with_back, comment_keyboard

MANAGER, DELIVERY, COMMENT = range(3)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/aW2ZfM6.jpeg",
        caption="Выберите менеджера:",
        reply_markup=manager_keyboard()
    )
    return MANAGER

async def select_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    manager = query.data.replace("manager_", "")
    user_data[query.from_user.id] = {"manager": manager}
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/Bv1EmlH.jpeg",
        caption="Выберите тип доставки:",
        reply_markup=delivery_keyboard_with_back()
    )
    await query.delete_message()
    return DELIVERY

async def select_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    delivery = query.data.replace("delivery_", "")
    user_data[query.from_user.id]["delivery"] = delivery
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/6MjshN5.jpeg",
        caption="Напишите комментарий к доставке:",
        reply_markup=comment_keyboard()
    )
    await query.delete_message()
    return COMMENT

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    user_data[uid]["comment"] = update.message.text

    message = (
        f"{user_data[uid]['manager']}\n"
        f"{user_data[uid]['delivery']}\n"
        f"💬 Комментарий: {user_data[uid]['comment']}"
    )
    await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/aW2ZfM6.jpeg",
        caption="Данные отправлены. Начнем заново.\nВыберите менеджера:",
        reply_markup=manager_keyboard()
    )
    return MANAGER

async def back_to_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/aW2ZfM6.jpeg",
        caption="Выберите менеджера:",
        reply_markup=manager_keyboard()
    )
    await query.delete_message()
    return MANAGER

async def back_to_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://i.imgur.com/Bv1EmlH.jpeg",
        caption="Выберите тип доставки:",
        reply_markup=delivery_keyboard_with_back()
    )
    await query.delete_message()
    return DELIVERY

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def get_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MANAGER: [
                CallbackQueryHandler(select_manager, pattern="^manager_")
            ],
            DELIVERY: [
                CallbackQueryHandler(select_delivery, pattern="^delivery_"),
                CallbackQueryHandler(back_to_manager, pattern="^back_to_manager$")
            ],
            COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment),
                CallbackQueryHandler(back_to_delivery, pattern="^back_to_delivery$")
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

def register_handlers(application):
    application.add_handler(get_conv_handler())