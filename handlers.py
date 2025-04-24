from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from config import CHANNEL_ID, IMAGES, DELIVERY_PRICES
from keyboard import manager_keyboard, delivery_keyboard, comment_keyboard

CHOOSE_MANAGER, CHOOSE_DELIVERY, WRITE_COMMENT = range(3)

user_data = {}
delivery_stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=IMAGES["choose_manager"],
        caption="💬 Выберите менеджера:",
        reply_markup=manager_keyboard()
    )
    return CHOOSE_MANAGER

async def choose_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    manager = query.data.replace("manager_", "")

    user_data[query.from_user.id] = {"manager": manager}

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=IMAGES["choose_delivery"],
            caption=f"{manager}\n\n📦 Выберите тип доставки:"
        ),
        reply_markup=delivery_keyboard()
    )
    return CHOOSE_DELIVERY

async def choose_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    manager = user_data.get(user_id, {}).get("manager", "❓")

    if query.data == "back_to_manager":
        user_data.pop(user_id, None)
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=IMAGES["choose_manager"],
                caption="💬 Выберите менеджера:"
            ),
            reply_markup=manager_keyboard()
        )
        return CHOOSE_MANAGER

    delivery = query.data.replace("delivery_", "")
    user_data[user_id]["delivery"] = delivery

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=IMAGES["choose_comment"],
            caption="💬 Введите комментарий:"
        ),
        reply_markup=comment_keyboard()
    )
    return WRITE_COMMENT

async def back_to_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    manager = user_data.get(user_id, {}).get("manager", "❓")

    await update.callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=IMAGES["choose_delivery"],
            caption=f"{manager}\n\n📦 Выберите тип доставки:"
        ),
        reply_markup=delivery_keyboard()
    )
    return CHOOSE_DELIVERY

async def write_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = user_data.get(user_id, {})
    comment = update.message.text.strip()

    if not comment:
        await update.message.reply_text("❗ Пожалуйста, введите комментарий.")
        return WRITE_COMMENT

    data["comment"] = comment
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    manager = data.get("manager")
    delivery = data.get("delivery")
    amount = DELIVERY_PRICES.get(delivery, 0)

    if manager not in delivery_stats:
        delivery_stats[manager] = []

    delivery_stats[manager].append({
        "type": delivery,
        "amount": amount
    })

    text = (
        f"🕒 {now}\n\n"
        f"*Менеджер:* {manager}\n"
        f"*Тип:* {delivery}\n"
        f"*Комментарий:* {comment}"
    )

    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка отправки в канал: {e}")
        return ConversationHandler.END

    await update.message.reply_photo(
        photo=IMAGES["choose_delivery"],
        caption=f"✅ Успешно отправлено!\n\n{manager}\n\n📦 Выберите тип доставки:",
        reply_markup=delivery_keyboard()
    )
    return CHOOSE_DELIVERY