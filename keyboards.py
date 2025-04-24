#keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def manager_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 Даниил", callback_data="manager_🔴 Даниил")],
        [InlineKeyboardButton("🟢 Дима", callback_data="manager_🟢 Дима")],
        [InlineKeyboardButton("🔵 Никита", callback_data="manager_🔵 Никита")]
    ])

def delivery_keyboard_with_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("OZON/WB/ТИПОГРАФИЯ", callback_data="delivery_📦 OZON/WB/ТИПОГРАФИЯ")],
        [InlineKeyboardButton("ЛАРГУС/ПАКЕТЫ", callback_data="delivery_📦 ЛАРГУС/ПАКЕТЫ")],
        [InlineKeyboardButton("ПО ГОРОДУ", callback_data="delivery_📦 ПО ГОРОДУ")],
        [InlineKeyboardButton("СДЭК", callback_data="delivery_📦 СДЭК")],
        [InlineKeyboardButton("СЕРВИС", callback_data="delivery_📦 СЕРВИС")],
        [InlineKeyboardButton("СКЛАД", callback_data="delivery_📦 СКЛАД")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back_to_manager")]
    ])

def comment_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Назад", callback_data="back_to_delivery")]
    ])