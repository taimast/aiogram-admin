from typing import Iterable

from aiogram import Dispatcher, Router, F

from .admin_menu import register_admin
from .bot_settings import register_bot_settings
from .chat_menu import register_chat
from .send_mail import register_send_mail
from .statistics_menu import register_statistics
from aiogram_admin.filters.admin import IsAdmin
router = Router()


def register_admin_handlers(dp: Dispatcher, admins: Iterable[int], super_admins: Iterable[int]):
    router.message.filter(F.from_user.id.in_(admins) | F.from_user.id.in_(super_admins))
    router.callback_query.filter(F.from_user.id.in_(admins) | F.from_user.id.in_(super_admins))

    register_admin(router, admins, super_admins)
    register_chat(router)
    register_send_mail(router)
    register_bot_settings(router)
    register_statistics(router)
    dp.include_router(router)
