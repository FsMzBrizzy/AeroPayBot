import asyncio
import logging
import os
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, LabeledPrice, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


def read_env(*names: str) -> Optional[str]:
    """Return the first environment variable value that is set."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


BOT_TOKEN = read_env("BOT_TOKEN", "TELEGRAM_BOT_TOKEN")
PROVIDER_TOKEN = read_env("PROVIDER_TOKEN", "PAYMENT_PROVIDER_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("Telegram bot token missing! Set BOT_TOKEN or TELEGRAM_BOT_TOKEN.")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)


class CustomAmount(StatesGroup):
    waiting_for_amount = State()


amounts = ["$25", "$50", "$100", "$200", "Custom", "Back"]

kb_amount = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=a)] for a in amounts],
    resize_keyboard=True,
    one_time_keyboard=True,
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/stats"), KeyboardButton(text="/broadcast")],
        [KeyboardButton(text="/addkey"), KeyboardButton(text="/listkeys")],
    ],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Owner panel active!", reply_markup=admin_kb)
    else:
        await message.answer("Welcome to GiftBot V1!\nChoose a plan:", reply_markup=kb_amount)


@dp.message(lambda m: m.text and m.text in ["$25", "$50", "$100", "$200"])
async def send_invoice(message: types.Message):
    if not PROVIDER_TOKEN:
        await message.answer(
            "Payments are not configured yet. Please contact support or try again later."
        )
        return

    amount = int(message.text.replace("$", ""))
    months = {25: 1, 50: 3, 100: 6, 200: 999}[amount]
    duration = "Lifetime" if months == 999 else f"{months} Month{'s' if months > 1 else ''}"

    prices = [LabeledPrice(label=f"{duration} VIP", amount=amount * 100)]
    await message.answer_invoice(
        title="VIP Access",
        description="Unlock premium features",
        payload="vip-access",
        provider_token=PROVIDER_TOKEN,
        currency="USD",
        prices=prices,
        start_parameter="vip",
    )


async def main():
    logging.info("Starting AeroPay bot polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
