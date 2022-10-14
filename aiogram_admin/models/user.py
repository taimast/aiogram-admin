from dataclasses import dataclass
from typing import Sequence


@dataclass
class BaseUser:
    id: int
    username: str
    first_name: str
    last_name: str

    @classmethod
    async def all(cls) -> Sequence['BaseUser']:
        raise NotImplementedError

    @classmethod
    async def count_all(cls) -> int:
        """Count all users in database"""
        raise NotImplementedError

    @classmethod
    async def count_new_today(cls) -> int:
        """Count new users today"""
        raise NotImplementedError
