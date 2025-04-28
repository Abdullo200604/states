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

class Registration(StatesGroup):
    name = State()
    fam = State()
    age = State()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.name)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n"
                         f"Ismingizni jo'nating!")

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text

    if user_name.isalpha():
        await state.set_state(Registration.fam)
        await message.answer("Ismingiz qabul qilindi, Familiyangizni kiriting")
    else:
        await message.answer("Ism faqat harflardan iborat bo'lsin, ismingizni qayta jo'nating")

@dp.message(Registration.fam, F.text == "/help")
async def help_in_fam(message: Message, state: FSMContext):
    await message.answer("siz familiyani kiritishingiz kk")

@dp.message(Registration.fam)
async def help_in_fam(message: Message, state: FSMContext):
    await state.set_state(Registration.age)
    await message.answer("Familiyangiz qabul qilindi, yoshingizni kiriting")

@dp.message(Registration.age)
async def help_in_fam(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("sizning ism, fam, yosgingiz qabul qilindi")

@dp.message(F.text == "/help")
async def help_handler(message: Message, state: FSMContext):
    await message.answer("Sizga tez orada 103 keladi")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())