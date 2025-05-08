from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.methods.refund_star_payment import RefundStarPayment
from aiogram.types import Message

from config import MESSAGES
from loader import bot

router = Router(name=__name__)


@router.message(Command("refund"))
async def process_refund(message: Message) -> None:
    """
    Process payment refund request.

    Args:
        message (Message): Message containing command and transaction ID
        Format: /refund <transaction_id>

    Sends:
        - Success/failure confirmation
        - Error message if format is invalid
    """
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer(MESSAGES['invalid_command'])
        await message.delete()
        return

    transaction_id = parts[1]
    try:
        result = await bot(RefundStarPayment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        ))

        await message.answer(
            MESSAGES['refund_success'] if result else MESSAGES['refund_fail']
        )
        await message.delete()
    except TelegramAPIError:
        await message.answer(MESSAGES['refund_fail'])
        await message.delete()
