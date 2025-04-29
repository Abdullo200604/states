import asyncio
import logging

from aiogram import types
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN
from sql import save_user_data
class Form(StatesGroup):
    name = State()
    age = State()
class Registration(StatesGroup):
    name = State()
    phone = State()
    age = State()

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.name)
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\n"
        f"Iltimos, ismingizni yuboring."
    )
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.next()
    await message.reply("Yoshingizni kiriting:")

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    save_user_data(data['name'], int(data['age']))
    await message.reply("Ma'lumotlaringiz saqlandi!")
    await state.finish()

@dp.message(Registration.name, F.text == "/help")
async def help_name(message: Message, state: FSMContext):
    await message.answer("Siz hozir ismingizni kiritishingiz kerak. Ism faqat harflardan iborat bo'lishi lozim.")

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text

    if user_name.isalpha():
        await state.set_state(Registration.phone)
        await message.answer("Ism qabul qilindi. Endi telefon raqamingizni yuboring. (faqat raqamlar)")
    else:
        await message.answer("Ism faqat harflardan iborat bo'lishi kerak. Iltimos, qaytadan yuboring.")

@dp.message(Registration.phone, F.text == "/help")
async def help_phone(message: Message, state: FSMContext):
    await message.answer("Siz hozir telefon raqamingizni kiritishingiz kerak. Misol uchun: 998901234567 ko'rinishida.")

@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):
    user_age = message.text

    if user_age.isdigit() and 0 < int(user_age) < 120:
        data = await state.get_data()
        save_user_data(data["name"], data["phone"], int(user_age))
        await state.clear()
        await message.answer("Ismingiz, telefon raqamingiz va yoshingiz muvaffaqiyatli saqlandi!")
    else:
        await message.answer("Yosh faqat raqamda va mantiqan to'g'ri bo'lishi kerak. Qaytadan kiriting.")
@dp.message(Registration.phone)
async def get_phone(message: Message, state: FSMContext):
    user_phone = message.text

    if user_phone.isdigit() and len(user_phone) == 12:
        await state.set_state(Registration.age)
        await message.answer("Telefon raqamingiz qabul qilindi. Endi yoshingizni kiriting.")
    else:
        await message.answer("Telefon raqami faqat 12 ta raqamdan iborat bo'lishi kerak (998 bilan boshlang). Qaytadan yuboring.")

@dp.message(Registration.age, F.text == "/help")
async def help_age(message: Message, state: FSMContext):
    await message.answer("Siz hozir yoshingizni raqamda kiritishingiz kerak. Masalan: 18, 25 va h.k.")

@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):
    user_age = message.text

    if user_age.isdigit() and 0 < int(user_age) < 120:
        await state.clear()
        await message.answer("Ismingiz, telefon raqamingiz va yoshingiz muvaffaqiyatli qabul qilindi!")
    else:
        await message.answer("Yosh faqat raqamda va mantiqan to'g'ri bo'lishi kerak. Qaytadan kiriting.")

@dp.message(F.text == "/help")
async def help_default(message: Message, state: FSMContext):
    await message.answer("Siz noto'g'ri joyda /help yubordingiz. Iltimos, kerakli ma'lumotni kiriting.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
