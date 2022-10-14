import asyncio
from typing import Sequence

import pytest
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_admin import setup_admin_handlers
from aiogram_admin.models import BaseSubsChat, BaseUser


@pytest.fixture
def bot():
    return Bot(token='5420708957:AAEErFtz2mdpGev-o139u8mlJetpp5whXPE')


@pytest.fixture
def dispatcher():
    storage = MemoryStorage()
    return Dispatcher(storage=storage)


class SubsChat(BaseSubsChat):
    @classmethod
    async def all(cls):
        return [cls(id=1, chat_id=2, skin='defaurler', )]


class User(BaseUser):


    @classmethod
    async def count_all(cls) -> int:
        """Count all users in database"""
        return 2

    @classmethod
    async def count_new_today(cls) -> int:
        """Count new users today"""
        return 3

    @classmethod
    async def all(cls) -> Sequence['User']:
        return [cls(id=269019356, username='test', first_name='test', last_name='test'),
                cls(id=5050812985, username='test', first_name='test', last_name='test')]

@pytest.mark.asyncio
async def test_start(dispatcher: Dispatcher, bot: Bot):
    dispatcher.message.filter(F.chat.type == "private")
    await setup_admin_handlers(
        dispatcher,
        [5050812985],
        SubsChat=SubsChat,
        User=User,
    )

    # await asyncio.wait_for(dispatcher.start_polling(
    #     bot,
    #     skip_updates=True,
    #     allowed_updates=dispatcher.resolve_used_update_types(),
    # ), timeout=100)
