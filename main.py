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
from sql import save_user_data

#bu state ya'ni o'qilishi stet ekan bilvol
class Registration(StatesGroup):
    name = State()
    phone = State()
    age = State()

dp = Dispatcher()

# pastdagi codni nima ekanini bilmasen codnga tegma!
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\n"
        f"Iltimos, ismingizni yuboring."
    )

#ism uchun help kamandasini foalashtiradi
@dp.message(Registration.name, F.text == "/help")
async def help_name(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiritishingiz kerak. U faqat harflardan iborat bo'lishi lozim.")

# bu pastdagi cod foydalanuvchini ismini oladi
@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text
    if user_name.isalpha():
        await state.update_data(name=user_name)
        await state.set_state(Registration.phone)
        await message.answer("Ism qabul qilindi. Endi telefon raqamingizni yuboring. (998 bilan boshlang, 12 ta raqam)")
    else:
        await message.answer("Ism faqat harflardan iborat bo'lishi kerak. Iltimos, qaytadan yuboring.")

# bu cod esa foydalanuvchini no'merini olayotganda ishga tushadi
@dp.message(Registration.phone, F.text == "/help")
async def help_phone(message: Message, state: FSMContext):
    await message.answer("Telefon raqamni 998 bilan boshlanib, 12 ta raqam bo'lishi kerak. Masalan: 998901234567")

# bu pastdagi cod foydalanuvchini no'merini oladi
@dp.message(Registration.phone)
async def get_phone(message: Message, state: FSMContext):
    user_phone = message.text
    if user_phone.isdigit() and len(user_phone) == 12 and user_phone.startswith("998"):
        await state.update_data(phone=user_phone)
        await state.set_state(Registration.age)
        await message.answer("Telefon raqam qabul qilindi. Endi yoshingizni yuboring.")
    else:
        await message.answer("Noto'g'ri raqam. 12 ta raqamdan iborat va 998 bilan boshlanishi kerak.")

# yosh sorayotganda help yuborsa shu funksiya ishlaydi
@dp.message(Registration.age, F.text == "/help")
async def help_age(message: Message, state: FSMContext):
    await message.answer("Yoshni raqamda kiriting. Masalan: 18, 25 va hokazo.")

# bu pastdagi cod foydalanuvchi yoshini oladi
@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):
    user_age = message.text
    if user_age.isdigit() and 0 < int(user_age) < 120:
        await state.update_data(age=int(user_age))
        data = await state.get_data()
        save_user_data(data["name"], data["phone"])
        await state.clear()
        await message.answer("Barcha ma'lumotlar muvaffaqiyatli saqlandi!")
    else:
        await message.answer("Yosh faqat raqamda va 0 dan katta, 120 dan kichik bo'lishi kerak.")

#bu pastdagi cod g'alati joyda /help yuborsa notog'ri deb beradi
@dp.message(F.text == "/help")
async def help_default(message: Message, state: FSMContext):
    await message.answer("Siz noto'g'ri joyda /help yubordingiz. Iltimos, kerakli maydonga mos tarzda foydalaning.")

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
