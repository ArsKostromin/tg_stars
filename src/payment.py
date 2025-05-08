from aiogram import Router, F, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from config import STARS_AMOUNT, MESSAGES
from loader import bot
from src.keyboards import star_amount_keyboard
router = Router(name=__name__)
from aiogram import types


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Выберите количество звёзд для покупки:", reply_markup=star_amount_keyboard())


@router.callback_query(F.data.startswith("pay:"))
async def handle_star_payment_callback(callback: types.CallbackQuery):
    amount = int(callback.data.split(":")[1])
    prices = [LabeledPrice(label=f'{amount} Stars', amount=amount)]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f'Stars Payment: {amount}',
        description='Оплата звёзд для пополнения баланса.',
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter='stars-payment',
        payload=f'{callback.from_user.id}:{amount}'  # 👈 в payload сохраняем user_id и amount
    )
    await callback.answer()



@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    """
    Validate the pre-checkout query before payment.

    Args:
        pre_checkout_query (PreCheckoutQuery): Pre-checkout query to validate
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


import httpx

STAR_PRICE_RUB = 1.7

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    user_id, amount = payment_info.invoice_payload.split(":")

    # Отправка запроса в backend
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://server2.anonixvpn.space/payments/stars/",
            json={"user_id": user_id, "amount": amount*STAR_PRICE_RUB}
        )

    await message.answer(
        MESSAGES['payment_success'].format(
            amount=amount,
            transaction_id=html.quote(payment_info.telegram_payment_charge_id)
        )
    )
