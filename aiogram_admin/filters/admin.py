from typing import Any

from aiogram import types
from aiogram.filters import BaseFilter


class IsAdmin(BaseFilter):

    def __init__(self, admins: list[int], super_admins: list[int]):
        self.admins = admins
        self.super_admins = super_admins

    async def __call__(self, update: types.CallbackQuery | types.Message) -> dict[str, Any] | bool:
        if update.from_user.id in self.admins:
            return {"is_admin": True, "is_super_admin": False}
        elif update.from_user.id in self.super_admins:
            return {"is_admin": True, "is_super_admin": True}
        return False
