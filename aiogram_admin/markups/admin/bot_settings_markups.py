from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_admin import config


def bot_setting_start(bot_running: bool):
    keywords = [
        ("🚫 Приостановить", "stop_bot") if bot_running else ("▶ Запустить", "run_bot"),
        ("🔃 Перезапустить", 'restart_bot'),
        ("⬅️ Назад", config.ADMIN_COMMAND),
    ]
    builder = InlineKeyboardBuilder()
    for keyword, payload in keywords:
        builder.button(text=keyword, callback_data=payload)
        builder.adjust(1)
    return builder.as_markup()
