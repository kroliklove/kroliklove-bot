# bot.py
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import BOT_TOKEN, OFFER_URL, POLICY_URL, COURSES

logging.basicConfig(level=logging.INFO)

# Настраиваем прокси через переменные окружения
os.environ['HTTP_PROXY'] = 'http://proxy.pythonanywhere.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.pythonanywhere.com:8080'

dp = Dispatcher()
accepted_users = set()

# === КЛАВИАТУРЫ ===
def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Оферта", url=OFFER_URL)
    builder.button(text="🔒 Политика", url=POLICY_URL)
    builder.button(text="✅ Согласен", callback_data="agree")
    builder.adjust(1)
    return builder.as_markup()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🧘‍♀️ Купить курс", callback_data="buy")
    builder.button(text="📞 Поддержка", callback_data="support")
    builder.adjust(1)
    return builder.as_markup()

def get_courses_keyboard():
    builder = InlineKeyboardBuilder()
    for course_id, course_data in COURSES.items():
        builder.button(
            text=f"{course_data['name']} — {course_data['price']}₽",
            callback_data=course_id
        )
    builder.button(text="⬅️ Назад", callback_data="nazad")
    builder.adjust(1)
    return builder.as_markup()

# === ЗАПУСК ===
async def main():
    bot = Bot(token=BOT_TOKEN)
    
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        if message.from_user.id in accepted_users:
            await message.answer("Добро пожаловать! 🎉", reply_markup=get_main_keyboard())
        else:
            await message.answer(
                "Привет! 👋 Ознакомься с документами и нажми «Согласен»:",
                reply_markup=get_start_keyboard()
            )

    @dp.callback_query(lambda c: c.data == "agree")
    async def process_agree(callback_query: types.CallbackQuery):
        accepted_users.add(callback_query.from_user.id)
        await callback_query.message.edit_text(
            "Спасибо! Теперь вы можете пользоваться ботом:",
            reply_markup=get_main_keyboard()
        )

    @dp.callback_query(lambda c: c.data == "buy")
    async def process_buy(callback_query: types.CallbackQuery):
        if callback_query.from_user.id not in accepted_users:
            await callback_query.answer("⚠️ Сначала примите оферту!", show_alert=True)
            return
        await callback_query.message.edit_text("Выберите курс:", reply_markup=get_courses_keyboard())

    @dp.callback_query(lambda c: c.data in COURSES.keys())
    async def process_buy_course(callback_query: types.CallbackQuery):
        course = COURSES[callback_query.data]
        builder = InlineKeyboardBuilder()
        builder.button(text="💳 Оплатить", callback_data=f"pay_{callback_query.data}")
        builder.button(text="⬅️ Назад", callback_data="nazad")
        builder.adjust(1)
        await callback_query.message.edit_text(
            f"🧘‍♀️ {course['name']}\n💰 {course['price']}₽\n⏱ {course['duration']}\n📝 {course['description']}",
            reply_markup=builder.as_markup()
        )

    @dp.callback_query(lambda c: c.data.startswith("pay_"))
    async def process_payment(callback_query: types.CallbackQuery):
        course_id = callback_query.data.replace("pay_", "")
        course = COURSES[course_id]
        await callback_query.answer(
            f"⏳ Оплата {course['name']} ({course['price']}₽) — скоро будет!",
            show_alert=True
        )

    @dp.callback_query(lambda c: c.data == "nazad")
    async def process_back(callback_query: types.CallbackQuery):
        await callback_query.message.edit_text("Главное меню:", reply_markup=get_main_keyboard())

    @dp.callback_query(lambda c: c.data == "support")
    async def process_support(callback_query: types.CallbackQuery):
        await callback_query.answer("📞 Поддержка: @твой_аккаунт", show_alert=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())