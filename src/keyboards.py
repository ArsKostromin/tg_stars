from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def star_amount_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ 1", callback_data="pay:1"),
            InlineKeyboardButton(text="⭐ 100", callback_data="pay:100"),
            InlineKeyboardButton(text="⭐ 500", callback_data="pay:500"),
        ]
    ])