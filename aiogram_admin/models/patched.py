from typing import Any, Optional, List

from aiogram import Dispatcher as _Dispatcher, Bot
from aiogram.dispatcher.dispatcher import DEFAULT_BACKOFF_CONFIG
from aiogram.utils.backoff import BackoffConfig


class Dispatcher(_Dispatcher):
    __extra_data__: dict

    async def start_polling(
            self,
            *bots: Bot,
            polling_timeout: int = 10,
            handle_as_tasks: bool = True,
            backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
            allowed_updates: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> None:
        kwargs.update(self.__extra_data__)
        return await super().start_polling(
            *bots,
            polling_timeout=polling_timeout,
            handle_as_tasks=handle_as_tasks,
            backoff_config=backoff_config,
            allowed_updates=allowed_updates,
            **kwargs
        )
