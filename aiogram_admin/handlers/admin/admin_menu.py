from typing import Iterable

from aiogram import Router, types
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionSender

from aiogram_admin import config
from aiogram_admin import utils
from aiogram_admin.markups.admin import admin_markups

router = Router()


class ExportUsers(StatesGroup):
    choice_send_type = State()
    finish = State()


async def admin_start(message: types.CallbackQuery | types.Message, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Админ меню", reply_markup=admin_markups.admin_start())


async def export_users_send_type(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"В каком виде экспортировать пользователей",
                              reply_markup=admin_markups.export_users_send_type())
    await state.set_state(ExportUsers.finish)


async def export_users_finish(call: types.CallbackQuery, state: FSMContext):
    # todo L2 14.10.2022 14:57 taima:
    result = await utils.export_users(_to=call.data)
    if call.data == "text":
        async with ChatActionSender.typing(bot=call.message.via_bot, chat_id=call.from_user.id):
            await utils.split_sending(call.message, result)
    else:
        async with ChatActionSender.upload_document(bot=call.message.via_bot, chat_id=call.from_user.id):
            await call.message.answer_document(result)
    await call.message.answer("Пользователи выгружены", reply_markup=admin_markups.back())


def register_admin(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(admin_start, Command(commands=config.ADMIN_COMMAND), StateFilter("*"))
    callback(admin_start, Text(config.ADMIN_COMMAND), StateFilter("*"))
    callback(export_users_send_type, Text("export_users"), StateFilter("*"))
    callback(export_users_finish, StateFilter(ExportUsers.finish))
