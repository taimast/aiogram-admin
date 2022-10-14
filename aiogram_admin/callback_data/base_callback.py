from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    all = "all"
    view = "view"
    create = "create"
    delete = "delete"
    edit = "edit"
    buy = "buy"
    get = "get"


class ChatCallback(CallbackData, prefix="channel"):
    pk: Optional[int]
    action: str
