from aiogram import Router, types, Bot
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown as md

from aiogram_admin.markups.common import common_markups
from aiogram_admin.middleware.language import gettext as _
from aiogram_admin.utils import is_subscribed_to_chat, TempData

router = Router()


async def check_subscribe(call: types.CallbackQuery, state: FSMContext, bot: Bot, temp_data: TempData):
    await state.clear()
    if await is_subscribed_to_chat(call.from_user.id, bot, temp_data.subscription_channels):
        await call.message.answer(_("✅ Подписки найдены, введите {} чтобы продолжить").format(md.hpre("start")),
                                  reply_markup=common_markups.check_subscribe())
        return True
    await call.answer(_("❌ Ты подписался не на все каналы"), show_alert=True)
    return False


def register_common(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(check_subscribe, Text("check_subscribe"), StateFilter("*"))
