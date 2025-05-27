from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def star_amount_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ 1", callback_data="pay:1"),
            InlineKeyboardButton(text="⭐ 15", callback_data="pay:15"),
            InlineKeyboardButton(text="⭐ 27", callback_data="pay:27"),
            InlineKeyboardButton(text="⭐ 48", callback_data="pay:48"),

        ]
    ])