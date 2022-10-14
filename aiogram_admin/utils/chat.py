import re

from aiogram import Bot
from loguru import logger

from aiogram_admin.models.chat import BaseSubsChat


def parse_channel_link(text: str) -> tuple[str, str]:
    skin, username = text.split()
    if '@' in username:
        username = username.replace('@', '')
    else:
        try:
            username = re.findall(r"t\.me/(.+)", username)[0]
        except Exception as e:
            logger.warning(e)
    return skin, username


async def is_subscribed_to_chat(user_id, bot: Bot, subscription_channels: list[BaseSubsChat]) -> bool:
    """
    :param user_id:
    :param bot:
    :param subscription_channels: Unique identifier for the target chat or username of the target supergroup or channel (in the format :code:`@channelusername`)
    :return: Returns :code:`True` if the user is a member of the chat
    """
    for chat in subscription_channels:
        try:
            member = await bot.get_chat_member(chat.chat_id, user_id)
            if member.status in ('left', 'kicked'):
                return False
        except Exception as e:
            logger.warning(f"{chat}|{e}")
            pass
    return True
