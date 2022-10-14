from dataclasses import dataclass
from typing import TypeAlias

ChatID: TypeAlias = str | int  # @username or id


@dataclass
class BaseSubsChat:
    id: str | int
    chat_id: ChatID
    skin: str

    @classmethod
    async def get(cls, pk: int | str) -> 'BaseSubsChat':
        """Get chat from database"""
        raise NotImplementedError

    async def delete(self) -> None:
        """Delete chat from database"""
        raise NotImplementedError

    @classmethod
    async def create(cls, skin: str, username: str) -> 'BaseSubsChat':
        """Create chat in database"""
        raise NotImplementedError

    @classmethod
    async def all(cls) -> list['BaseSubsChat']:
        """Get all chats from database"""
        return []
