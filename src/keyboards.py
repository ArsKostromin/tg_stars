from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def star_amount_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ 550~7$", callback_data="pay:550"),
            InlineKeyboardButton(text="⭐ 1200~15$", callback_data="pay:1200"),
            InlineKeyboardButton(text="⭐ 2100~27$", callback_data="pay:2100"),
            InlineKeyboardButton(text="⭐ 3700~48$", callback_data="pay:3700"),
        ],
        [
            InlineKeyboardButton(text="💰 Ввести сумму", callback_data="pay:custom")
        ]
    ])
