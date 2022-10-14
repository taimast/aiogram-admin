from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger

from aiogram_admin import models
from aiogram_admin.callback_data.base_callback import ChatCallback, Action
from aiogram_admin.markups.admin import channel_markups, admin_markups
from aiogram_admin.utils import parse_channel_link, TempData

router = Router()


class NewChat(StatesGroup):
    done = State()


class NewSponsorChat(StatesGroup):
    done = State()


async def view_chats(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    chats = await models.BaseSubsChat.all()
    await call.message.answer(f"Все чаты для обязательной подписки:",
                              reply_markup=channel_markups.view_channels(chats))


async def create_chat(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Добавьте бота в чат и сделайте администратором, чтобы проверять подписки.\n"
                              f"Введите ссылку на канал. "
                              f"Введите ссылку по которому должны будут пройти пользователи и через пробел"
                              f" фактическую ссылку на канал для проверки ботом\n"
                              f"Например:\n"
                              f"https://t.me/+bIBc0e-525k2MThi https://t.me/mychannel \nили\n"
                              f"https://t.me/mychannel https://t.me/mychannel",
                              reply_markup=admin_markups.back())
    await state.set_state(NewChat.done)


async def create_chat_done(message: types.Message, state: FSMContext, temp_data: TempData):
    try:
        await state.clear()
        skin, username = parse_channel_link(message.text)
        channel = await models.BaseSubsChat.create(skin=skin, username=username)
        temp_data.subscription_channels.append(channel)
        await message.answer(f"Канал для подписки: {channel}\n успешно добавлен", reply_markup=admin_markups.back())
    except Exception as e:
        logger.warning(e)
        await message.answer("Неправильный ввод", reply_markup=admin_markups.back())


async def view_chat(call: types.CallbackQuery, callback_data: ChatCallback, state: FSMContext):
    await state.clear()
    _chat = await models.BaseSubsChat.get(pk=callback_data.pk)
    await call.message.answer(f"{_chat}",
                              reply_markup=channel_markups.touch_channel(_chat))


async def delete_chat(call: types.CallbackQuery,
                      callback_data: ChatCallback,
                      state: FSMContext,
                      temp_data: TempData):
    await state.clear()
    await state.update_data(delete_chat=callback_data.pk)

    channel = await models.BaseSubsChat.get(pk=callback_data.pk)
    await channel.delete()
    temp_data.subscription_channels.remove(channel)

    await call.message.answer(f"Канал для подписки: {channel} успешно удален", reply_markup=admin_markups.back())


def register_chat(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(view_chats, ChatCallback.filter(F.action == Action.all), StateFilter("*"))
    callback(create_chat, ChatCallback.filter(F.action == Action.create), StateFilter("*"))
    message(create_chat_done, StateFilter(NewChat.done))
    callback(view_chat, ChatCallback.filter(F.action == Action.view), StateFilter("*"))
    callback(delete_chat, ChatCallback.filter(F.action == Action.delete), StateFilter("*"))
