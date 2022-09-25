from aiogram.types import CallbackQuery

from keyboards.inline.mailing_settings import mailing_setting
from loader import dp


@dp.callback_query_handler(text="settings")
async def get_setting(call: CallbackQuery):
    await call.message.answer("Вы перешли в раздел с настройками рассылки отчетов",
                              reply_markup=await mailing_setting())


@dp.callback_query_handler(text="morning")
@dp.callback_query_handler(text="afternoon")
@dp.callback_query_handler(text="evening")
async def morning_mailing(call: CallbackQuery):
    await call.answer("Настройки пременены")
