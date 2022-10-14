from pydantic import BaseModel

from aiogram_admin.models.chat import BaseSubsChat
from aiogram_admin.utils.send_mail import MailSender


class TempData(BaseModel):
    """Данные для временного хранения в памяти"""
    subscription_channels: list[BaseSubsChat] = []
    """ Список каналов для подписки """
    mail_sender: MailSender | None = None
    """ Объект для отправки писем """
    bot_running: bool = True
    """ Флаг запуска бота """

    class Config:
        arbitrary_types_allowed = True
        copy_on_model_validation = False
