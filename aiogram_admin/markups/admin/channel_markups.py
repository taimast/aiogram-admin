from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_admin.callback_data.base_callback import ChatCallback, Action
from aiogram_admin.models import BaseSubsChat


def view_channels(channels: list[BaseSubsChat]):
    builder = InlineKeyboardBuilder()
    for c in channels:
        builder.button(
            text=f"{c}",
            callback_data=ChatCallback(pk=c.chat_id, action=Action.view)
        )
    builder.adjust(1)
    return builder.as_markup()


def touch_channel(channel):
    builder = InlineKeyboardBuilder()
    builder.button(text="✍ Удалить.", callback_data=ChatCallback(pk=channel.id, action=Action.delete))
    builder.button(text="⬅️ Назад", callback_data="admin")
    builder.adjust(1)
    return builder.as_markup()
