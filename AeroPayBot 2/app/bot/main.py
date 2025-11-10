import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_TOKEN = os.getenv("STRIPE_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in Railway Variables!")
if not STRIPE_TOKEN:
    raise ValueError("STRIPE_TOKEN missing! Must be pk_test_...")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)

# === DATABASE (in memory) ===
users = set()
keys = ["AERO2025VIP: permanent"]

# === STATES ===
class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_addkey = State()

class CustomAmount(StatesGroup):
    waiting_for_amount = State()

# === KEYBOARDS ===
amounts = ["$25", "$50", "$100", "$200", "Custom", "Back"]
kb_amount = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=a)] for a in amounts],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/stats"), KeyboardButton(text="/broadcast")],
        [KeyboardButton(text="/addkey"), KeyboardButton(text="/listkeys")]
    ],
    resize_keyboard=True
)

# === START ===
@dp.message(Command("start"))
async def start(message: types.Message):
    users.add(message.from_user.id)
    if message.from_user.id == OWNER_ID:
        await message.answer("Owner panel active!", reply_markup=admin_kb)
    else:
        await message.answer("Welcome to GiftBot V1!\nChoose a plan:", reply_markup=kb_amount)

# === FIXED PLANS ===
@dp.message(F.text.in_(["$25", "$50", "$100", "$200"]))
async def send_fixed_plan(message: types.Message):
    amount = int(message.text.replace("$", ""))
    months = {25:1, 50:3, 100:6, 200:999}[amount]
    duration = "Lifetime" if months == 999 else f"{months} Month{'s' if months > 1 else ''}"

    prices = [LabeledPrice(label=f"{duration} VIP", amount=amount * 100)]
    await message.answer_invoice(
        title=f"{duration} VIP Access",
        description=f"Get {duration.lower()} VIP key",
        payload=f"vip_{amount}_{message.from_user.id}",
        provider_token=STRIPE_TOKEN,
        currency="USD",
        prices=prices,
        start_parameter="vip"
    )

# === CUSTOM AMOUNT ===
@dp.message(F.text == "Custom")
async def custom_start(message: types.Message, state: FSMContext):
    await message.answer("Enter amount in USD (1–2000):\nExample: 1337", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CustomAmount.waiting_for_amount)

@dp.message(CustomAmount.waiting_for_amount)
async def process_custom(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text.strip().replace("$", ""))
        if not (1 <= amount <= 2000):
            await message.answer("Amount must be 1–2000")
            return
        prices = [LabeledPrice(label=f"Custom ${amount}", amount=amount * 100)]
        await message.answer_invoice(
            title="Custom VIP Access",
            description=f"Permanent VIP key for ${amount}",
            payload=f"custom_{amount}_{message.from_user.id}",
            provider_token=STRIPE_TOKEN,
            currency="USD",
            prices=prices,
            start_parameter="custom"
        )
        await state.clear()
    except ValueError:
        await message.answer("Send a valid number")

# === BACK ===
@dp.message(F.text == "Back")
async def back_to_menu(message: types.Message):
    await message.answer("Choose a plan:", reply_markup=kb_amount)

# === PAYMENT HANDLERS ===
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def payment_success(message: types.Message):
    amount = message.successful_payment.total_amount // 100
    key = f"AERO{amount}VIP"
    keys.append(f"{key}: permanent")
    await message.answer(
        f"Payment successful! ${amount}\n\n"
        f"Key `{key}` added as permanent!\n\n"
        f"Redeem at: https://www.aeroelite.shop/gift-card",
        parse_mode="Markdown"
    )

# === ADMIN COMMANDS ===
@dp.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id != OWNER_ID: return
    await message.answer(f"Statistics:\nUsers: {len(users)}\nPurchases: {len(keys)-1}\nRevenue: ${sum(int(k.split('AERO')[1].split('VIP')[0]) for k in keys if 'AERO' in k)}")

@dp.message(Command("listkeys"))
async def listkeys(message: types.Message):
    if message.from_user.id != OWNER_ID: return
    await message.answer("Active keys:\n" + "\n".join(keys))

@dp.message(Command("broadcast"))
async def broadcast_start(message: types.Message, state: FSMContext):
    if message.from_user.id != OWNER_ID: return
    await message.answer("Send message to broadcast:")
    await state.set_state(AdminStates.waiting_broadcast)

@dp.message(AdminStates.waiting_broadcast)
async def broadcast_send(message: types.Message, state: FSMContext):
    sent = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, message.text)
            sent += 1
        except: pass
    await message.answer(f"Sent to {sent} users")
    await state.clear()

@dp.message(Command("addkey"))
async def addkey_start(message: types.Message, state: FSMContext):
    if message.from_user.id != OWNER_ID: return
    await message.answer("Send key (KEYNAME: duration)")
    await state.set_state(AdminStates.waiting_addkey)

@dp.message(AdminStates.waiting_addkey)
async def addkey_save(message: types.Message, state: FSMContext):
    keys.append(message.text)
    await message.answer(f"Key added:\n{message.text}")
    await state.clear()

# === RUN ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
