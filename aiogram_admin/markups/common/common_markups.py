from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_admin.models import BaseSubsChat


def start() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    keywords = [
        ("🪙 Купить аккаунты", "buy_accounts"),
        ("🪪 Получить бесплатный тестовый доступ", "get_free_test"),
        ("📜 Подробная информация", "info"),
    ]
    for text, callback_data in keywords:
        builder.button(text=text, callback_data=callback_data)
    builder.adjust(1)
    return builder.as_markup()


def is_subscribed_to_channel(channels: list[BaseSubsChat],
                             callback_data: str = "check_subscribe") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for num, channel in enumerate(channels, 1):
        builder.button(text=_("Канал #{}").format(num), url=channel.skin)
    builder.button(text=_("✅ Я подписался"), callback_data=callback_data)
    builder.adjust(1)
    return builder.as_markup()


def check_subscribe() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='start', callback_data="start")
    return builder.as_markup()


def custom_back(callback_data: str | CallbackData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data=callback_data)
    return builder.as_markup()
