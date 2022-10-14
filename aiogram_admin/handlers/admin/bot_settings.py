import asyncio
import random

from aiogram import Router, types
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram_admin.markups.admin import bot_settings_markups
from aiogram_admin.utils import TempData

router = Router()


class SendMail(StatesGroup):
    preview = State()
    select = State()

    button = State()
    send = State()


async def bot_setting_start(call: types.CallbackQuery, state: FSMContext, temp_data: TempData):
    await state.clear()
    status = "✅ Запущен" if temp_data.bot_running else "🚫 Приостановлен"
    await call.message.answer("Панель управления ботом\n"
                              f"Статус бота:\n{status}",
                              reply_markup=bot_settings_markups.bot_setting_start(temp_data.bot_running))


async def start_bot_view(call):
    send_text = "🤖 Производиться запуск бота ожидайте...\n1"
    message = await call.message.answer(send_text)
    for text in ["Проверка целостности",
                 "Проверка конфигурации",
                 "Проверка базы данных",
                 "Проверка протоколов",
                 "Оптимизация"]:
        for sign in ["⏳", "⌛", "✅"]:
            await asyncio.sleep(random.uniform(0, 1))
            add_text = f"\n▶ {text} {sign}"
            await message.edit_text(f"{send_text}{add_text}")
        send_text += add_text


async def run_bot(call: types.CallbackQuery, temp_data: TempData):
    temp_data.bot_running = True
    await start_bot_view(call)
    await call.message.edit_reply_markup(bot_settings_markups.bot_setting_start(temp_data.bot_running))
    await call.message.answer("✅ Бот успешно запущен")


async def stop_bot(call: types.CallbackQuery, temp_data: TempData):
    temp_data.bot_running = False
    await call.message.edit_reply_markup(bot_settings_markups.bot_setting_start(temp_data.bot_running))
    edit_message = await call.message.answer("🕐 Приостановка бота")
    await asyncio.sleep(random.uniform(0, 1))
    await edit_message.edit_text("✅ Бот приостановлен")


async def restart_bot(call: types.CallbackQuery, temp_data: TempData):
    await call.message.answer("Перезапуск бота ожидайте...")
    temp_data.bot_running = False
    await start_bot_view(call)
    temp_data.bot_running = True
    await call.message.answer("Бот перезапущен")


def register_bot_settings(dp: Router):
    dp.include_router(router)
    callback = router.callback_query.register

    callback(bot_setting_start, Text("bot_settings"), StateFilter("*"))

    callback(run_bot, Text("run_bot"), StateFilter("*"))
    callback(stop_bot, Text("stop_bot"), StateFilter("*"))
    callback(restart_bot, Text("restart_bot"), StateFilter("*"))
