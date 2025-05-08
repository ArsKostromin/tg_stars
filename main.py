"""
Telegram Payment Bot with Stars Payment System

Features:
    - Stars payment processing
    - Invoice generation
    - Payment refund system

Usage:
    /start - Generate payment invoice
    /refund <transaction_id> - Refund a payment

Based on: https://habr.com/ru/articles/821415/
"""

import asyncio
import logging

from aiogram import Dispatcher

from loader import bot
from src.payment import router as payment_router
from src.refund import router as refund_router

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
dispatcher_logger = logging.getLogger('aiogram.dispatcher')
dispatcher_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(payment_router)
dp.include_router(refund_router)


async def main() -> None:
    """Initialize and start the bot."""
    try:
        await dp.start_polling(bot)
    finally:
        await dp.stop_polling()


if __name__ == '__main__':
    asyncio.run(main())
