import asyncio
from typing import TypeVar

from aiogram import types

MESSAGE_LIMIT = 4096
ReplyMarkup = TypeVar("ReplyMarkup", types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove,
                      types.ForceReply)


async def split_sending(message: types.Message,
                        answer_text: str,
                        reply_markup: ReplyMarkup = None):
    answer_length = len(answer_text)
    if answer_length > MESSAGE_LIMIT:
        for _from in range(0, answer_length, MESSAGE_LIMIT):
            _to = _from + MESSAGE_LIMIT
            if _to >= answer_length:
                await message.answer(answer_text[_from: _to], reply_markup=reply_markup)
            else:
                await message.answer(answer_text[_from:_to])
            await asyncio.sleep(0.5)
    else:
        await message.answer(answer_text, reply_markup=reply_markup)
