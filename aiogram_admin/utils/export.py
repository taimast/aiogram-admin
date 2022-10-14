import json
from typing import Literal

from aiogram.types import BufferedInputFile

from aiogram_admin import models


async def export_users(_to: Literal['text', 'txt', 'json']) -> BufferedInputFile | str:
    users = await models.BaseUser.all()
    users_list = [users.__dict__ for users in users]
    if _to == "text":
        user_value_list = list(map(lambda x: str(list(x.values())), users_list))
        result = "\n".join(user_value_list)
    elif _to == "txt":
        user_value_list = list(map(lambda x: str(list(x.values())), users_list))
        user_txt = "\n".join(user_value_list)
        result = BufferedInputFile(bytes(user_txt, "utf-8"), filename="users.txt")
    else:
        user_data = json.dumps(users_list, ensure_ascii=False, default=str)
        result = BufferedInputFile(bytes(user_data, "utf-8"),
                                   filename="users.json")
    return result
