from aiogram import types, Bot
from aiogram.filters import BaseFilter
from loguru import logger

from aiogram_admin.markups.common import common_markups
from aiogram_admin.utils import is_subscribed_to_chat, TempData


class ChannelSubscriptionFilter(BaseFilter):

    async def __call__(self, message: types.Message | types.CallbackQuery,
                       bot: Bot,
                       temp_data: TempData) -> bool:
        if isinstance(message, types.CallbackQuery):
            message = message.message
        user_id = message.from_user.id
        if not await is_subscribed_to_chat(user_id, bot, temp_data.subscription_channels):
            await message.delete()
            await message.answer(f"@{message.from_user.username}📍 Для того, чтобы пользоваться ботом, нужно подписаться на каналы:",
                                 reply_markup=common_markups.is_subscribed_to_channel(temp_data.subscription_channels))
            logger.trace("User {} is not subscribed to channels", user_id)
            return False
        logger.info("User {} is subscribed to channels", user_id)
        return True
