from aiogram import Router, F, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import httpx

from config import STARS_AMOUNT, MESSAGES
from loader import bot
from src.keyboards import star_amount_keyboard

router = Router(name=__name__)


# FSM для кастомного ввода
class PaymentStates(StatesGroup):
    waiting_for_custom_amount = State()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Выберите количество звёзд для покупки:", reply_markup=star_amount_keyboard())


@router.callback_query(F.data.startswith("pay:"))
async def handle_star_payment_callback(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]

    if action == "custom":
        await callback.message.answer("Введите количество звёзд, которое хотите купить (целое число):")
        await state.set_state(PaymentStates.waiting_for_custom_amount)
    else:
        amount = int(action)
        prices = [LabeledPrice(label=f'{amount} Stars', amount=amount)]

        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f'Stars Payment: {amount}',
            description='Оплата звёзд для пополнения баланса.',
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter='stars-payment',
            payload=f'{callback.from_user.id}:{amount}'
        )
        await callback.answer()


@router.message(PaymentStates.waiting_for_custom_amount)
async def handle_custom_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введите корректное положительное целое число.")
        return

    prices = [LabeledPrice(label=f'{amount} Stars', amount=amount)]

    await bot.send_invoice(
        chat_id=message.from_user.id,
        title=f'Stars Payment: {amount}',
        description='Оплата звёзд для пополнения баланса.',
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter='stars-payment',
        payload=f'{message.from_user.id}:{amount}'
    )

    await state.clear()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


STAR_PRICE_RUB = 0.013  # цена за 1 звезду в рублях

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    user_id, amount = payment_info.invoice_payload.split(":")

    amount = int(amount)

    # Отправка запроса в backend
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://server2.anonixvpn.space/payments/stars/",
            json={"user_id": user_id, "amount": amount * STAR_PRICE_RUB}
        )

    await message.answer(
        MESSAGES['payment_success'].format(
            amount=amount,
            transaction_id=html.quote(payment_info.telegram_payment_charge_id)
        )
    )
