from aiogram import Router, types, Bot
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from aiogram_admin.markups.admin import admin_markups
from aiogram_admin.markups.admin.admin_markups import send_mail_add_button_in_current
from aiogram_admin.utils import MailSender, MailStatus, TempData

router = Router()


class SendMail(StatesGroup):
    preview = State()
    select = State()

    button = State()
    send = State()


async def send_mail(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f"Перешлите мне сообщение с кнопками или Введите текст для рассылки всем пользователям",
                              reply_markup=admin_markups.back())
    await state.set_state(SendMail.preview)


async def send_mail_preview(message: types.Message, state: FSMContext):
    # print(message)
    if message.text:
        await state.update_data(mail=message.text)
    else:
        await state.update_data(mail=message.caption)
    if message.reply_markup:
        await send_mail_add_button(message, state)
        return
    await message.answer(message.text, reply_markup=admin_markups.send_mail_preview())
    await state.set_state(SendMail.select)


async def send_mail_add_button_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Перешлите мне список кнопок или отправьте мне список URL-кнопок в одном сообщении. "
                              "Следуйте этому формату:\n"
                              "Кнопка 1 - https://www.example1.com\n"
                              "Кнопка 2 - https://www.example2.com\n\n"
                              "Используйте разделитель |, чтобы добавить до трех кнопок в один ряд. Например:\n"
                              "Кнопка 1 - https://www.example1.com |\n"
                              "Кнопка 2 - https://www.example2.com\n"
                              "Кнопка 3 - https://www.example3.com |\n"
                              "Кнопка 4 - https://www.example4.com\n",
                              reply_markup=ReplyKeyboardRemove())
    await state.set_state(SendMail.button)


async def send_mail_add_button(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        if message.reply_markup:
            save_markup = message.reply_markup
            await state.update_data(markup=save_markup.dict())
            send_markup = send_mail_add_button_in_current(save_markup)
        else:
            save_markup = admin_markups.send_mail_add_button_save_keyboard(message.text)
            await state.update_data(markup=save_markup.dict())
            send_markup = admin_markups.send_mail_add_button(message.text)

        await message.answer(data["mail"], reply_markup=send_markup)
        await state.set_state(SendMail.select)
    except Exception as e:
        logger.exception(e)
        await message.answer("Произошла ошибка, повторите попытку")


async def send_mail_done(call: types.CallbackQuery, state: FSMContext, temp_data: TempData, bot: Bot):
    try:
        await call.message.answer("Идет отправка...")
        data = await state.get_data()
        await state.clear()
        sender = MailSender(bot=bot, message=call.message, mail=data.get("mail"), markup=data.get("markup"))
        if temp_data.mail_sender:
            temp_data.mail_sender.status = MailStatus.stop
        temp_data.mail_sender = sender
        await sender.send_mail()
    except Exception as e:
        logger.exception(e)
        await call.message.answer("Произошла ошибка, повторите попытку")


async def send_mail_pause(call: types.CallbackQuery, temp_data: TempData):
    temp_data.mail_sender.status = MailStatus.pause
    await temp_data.mail_sender.status_message.edit_reply_markup(
        admin_markups.send_mail_done(False)
    )


async def send_mail_continue(call: types.CallbackQuery, temp_data: TempData):
    temp_data.mail_sender.status = MailStatus.run
    await temp_data.mail_sender.status_message.edit_reply_markup(
        admin_markups.send_mail_done()
    )


async def send_mail_stop(call: types.CallbackQuery, temp_data: TempData):
    temp_data.mail_sender.status = MailStatus.stop


def register_send_mail(dp: Router):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    callback(send_mail, Text("send_mail"), StateFilter("*"))
    message(send_mail_preview, StateFilter(SendMail.preview))

    callback(send_mail_add_button_start, Text("add_button"), StateFilter(SendMail.select))
    message(send_mail_add_button, StateFilter(SendMail.button))

    callback(send_mail_done, Text("accept"), StateFilter(SendMail.select))
    callback(send_mail_pause, Text("pause_mail"), StateFilter("*"))
    callback(send_mail_continue, Text("continue_mail"), StateFilter("*"))
    callback(send_mail_stop, Text("stop_mail"), StateFilter("*"))
