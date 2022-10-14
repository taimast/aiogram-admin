from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger

from aiogram_admin import models
from aiogram_admin.markups.admin import statistics_markups, admin_markups

router = Router()


class SendMail(StatesGroup):
    preview = State()
    select = State()

    button = State()
    send = State()


async def statistics_start(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        all_count = await models.BaseUser.count_all()
        today_count = await models.BaseUser.count_new_today()

        await call.message.answer(
            f"📊 В боте зарегистрировано: {all_count}\n"
            f"📊 Новых пользователей за сегодня: {today_count}\n",
            reply_markup=admin_markups.back()
        )
    except Exception as e:
        logger.exception(e)


async def users_count(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    count = await models.BaseUser.count_all()
    await call.message.answer(f"В боте зарегистрировано: {count} 👥",
                              reply_markup=statistics_markups.back())


async def users_count_new(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    count = await models.BaseUser.count_new_today()
    await call.message.answer(f"Новых пользователей за сегодня: {count} 👥",
                              reply_markup=statistics_markups.back())


def register_statistics(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    # message = router.message.register

    callback(statistics_start, Text("statistics"), StateFilter("*"))
    callback(users_count, Text("users_count"), StateFilter("*"))
    callback(users_count_new, Text("users_count_new"), StateFilter("*"))
