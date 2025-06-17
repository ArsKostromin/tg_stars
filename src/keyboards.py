from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def star_amount_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ 77~1$", callback_data="pay:77"),
            InlineKeyboardButton(text="⭐ 1160~15", callback_data="pay:1160"),
            InlineKeyboardButton(text="⭐ 2080~27$", callback_data="pay:2080"),
            InlineKeyboardButton(text="⭐ 3700~48$", callback_data="pay:3700"),
        ],
        [
            InlineKeyboardButton(text="💰 Ввести свою сумму", callback_data="pay:custom")
        ]
    ])
