from typing import TypeAlias, Protocol, runtime_checkable

ChatID: TypeAlias = str | int  # @username or id


@runtime_checkable
class BaseSubsChat(Protocol):
    id: str | int
    chat_id: ChatID
    skin: str

    def __str__(self) -> str:
        return f"{self.chat_id} [{self.skin}]"

    @classmethod
    async def get(cls, pk: int | str) -> 'BaseSubsChat':
        """Get chat from database"""
        raise NotImplementedError

    async def delete(self) -> None:
        """Delete chat from database"""
        raise NotImplementedError

    @classmethod
    async def create(cls, skin: str, chat_id: ChatID) -> 'BaseSubsChat':
        """Create chat in database"""
        raise NotImplementedError

    @classmethod
    async def all(cls) -> list['BaseSubsChat']:
        """Get all chats from database"""
        return []
