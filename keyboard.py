#keyboard.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import MANAGERS, DELIVERY_TYPES

def manager_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(manager, callback_data=f"manager_{manager}")]
        for manager in MANAGERS
    ])

def delivery_keyboard():
    buttons = [
        [InlineKeyboardButton(delivery, callback_data=f"delivery_{delivery}")]
        for delivery in DELIVERY_TYPES
    ]
    buttons.append([InlineKeyboardButton("♻️ Сменить менеджера", callback_data="back_to_manager")])
    return InlineKeyboardMarkup(buttons)

def comment_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Назад", callback_data="back_to_delivery")]
    ])