from aiogram import Router, types
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionSender
from aiogram_admin import config
from aiogram_admin import utils
from aiogram_admin.filters.admin import IsAdmin
from aiogram_admin.markups.admin import admin_markups

router = Router()


class ExportUsers(StatesGroup):
    choice_send_type = State()
    finish = State()


async def admin_start(message: types.CallbackQuery | types.Message,is_super_admin:bool, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(f"Админ меню", reply_markup=admin_markups.admin_start(is_super_admin))


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


@router.callback_query(Text("add_admins"))
async def add_admins(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Введи id админов через пробел", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("add_admins")


@router.message(StateFilter("add_admins"))
async def add_admins_handler(message: types.Message, is_super_admin: bool, my_admins: list[int],
                             state: FSMContext):
    admins = message.text.split()
    for admin in admins:
        if admin.isdigit():
            admin = int(admin)
            my_admins.append(admin)

    await message.answer(f"Добавлены админы {admins}", reply_markup=admin_markups.admin_start(is_super_admin))
    await state.clear()


@router.callback_query(Text("delete_admins"))
async def delete_admins(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Введи id админов через пробел", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("delete_admins")


@router.message(StateFilter("delete_admins"))
async def delete_admins_handler(message: types.Message,  is_super_admin: bool, my_admins: list[int],
                                state: FSMContext):
    admins = message.text.split()
    for admin in admins:
        if admin.isdigit():
            admin = int(admin)
            my_admins.remove(admin)

    await message.answer(f"Удалены админы {admins}", reply_markup=admin_markups.admin_start(is_super_admin))
    await state.clear()


@router.callback_query(Text("admins"))
async def adminds(call: types.CallbackQuery, is_super_admin:bool,my_admins:list[int], state: FSMContext):
    await call.message.answer(f"Админы: {my_admins}",
                              reply_markup=admin_markups.admin_start(is_super_admin))


def register_admin(dp: Router, admins: list[int], super_admins: list[int]):
    dp.include_router(router)
    router.callback_query.filter(IsAdmin(admins, super_admins))
    router.message.filter(IsAdmin(admins, super_admins))

    callback = router.callback_query.register
    message = router.message.register

    message(admin_start, Command(commands=config.ADMIN_COMMAND), StateFilter("*"))
    callback(admin_start, Text(config.ADMIN_COMMAND), StateFilter("*"))
    callback(export_users_send_type, Text("export_users"), StateFilter("*"))
    callback(export_users_finish, StateFilter(ExportUsers.finish))
