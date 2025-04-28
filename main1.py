import asyncio
import logging

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import TOKEN

# Faqat 2 ta state
class Registration(StatesGroup):
    name = State()
    fam = State()

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.name)
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!\n"
        f"Iltimos, ismingizni jo'nating!"
    )

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text

    if user_name.isalpha():
        await state.set_state(Registration.fam)
        await message.answer("Ismingiz qabul qilindi. Endi familiyangizni kiriting.")
    else:
        await message.answer("Ism faqat harflardan iborat bo'lishi kerak. Iltimos, qaytadan kiriting.")

@dp.message(Registration.fam, F.text == "/help")
async def help_in_fam(message: Message, state: FSMContext):
    await message.answer("Familiyangizni kiritishingiz kerak!")

@dp.message(Registration.fam)
async def get_fam(message: Message, state: FSMContext):
    user_fam = message.text

    if user_fam.isalpha():
        await state.clear()
        await message.answer("Ism va familiyangiz muvaffaqiyatli qabul qilindi!")
    else:
        await message.answer("Familiya faqat harflardan iborat bo'lishi kerak. Iltimos, qaytadan kiriting.")

@dp.message(F.text == "/help")
async def help_handler(message: Message, state: FSMContext):
    await message.answer("Sizga yordam kerakmi? Tez orada 103 yetib boradi :)")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
