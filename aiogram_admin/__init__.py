from typing import Type, Iterable

from aiogram import Dispatcher

from aiogram_admin import models, config
from aiogram_admin.filters.channel_subscription_filter import ChannelSubscriptionFilter
from aiogram_admin.handlers.admin import register_admin_handlers
from aiogram_admin.handlers.common import register_common_handlers
from aiogram_admin.handlers.errors.errors_handlers import register_error
from aiogram_admin.models import BaseSubsChat, BaseUser
from aiogram_admin.utils import TempData

__all__ = (
    "setup_admin_handlers",
    "ChannelSubscriptionFilter",
    "BaseSubsChat",
    "BaseUser",
    "TempData",
)


async def setup_admin_handlers(dp: Dispatcher,
                               admins: Iterable[int],
                               super_admins: Iterable[int],
                               SubsChat: Type[models.BaseSubsChat],
                               User: Type[models.BaseUser],
                               admin_command: str = None,
                               temp_data: TempData = None) -> None:
    """
    Setup admin handlers
    :param dp:  Dispatcher
    :param admins:  Admins list
    :param SubsChat:  SubsChat model
    :param User:  User model
    :param temp_data:  TempData
    """
    models.BaseSubsChat = SubsChat
    models.BaseUser = User
    config.ADMIN_COMMAND = admin_command or config.ADMIN_COMMAND
    register_admin_handlers(dp, admins, super_admins)
    register_common_handlers(dp)
    if temp_data is None:
        temp_data = TempData(subscription_channels=await SubsChat.all())
    dp.workflow_data.update(temp_data=temp_data)
