import asyncio

from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.main_menu import main_keyboard
from keyboards.inline.report_settings import report_setting
from loader import dp, bot
from utils.misc.main_scripts import inference


@dp.callback_query_handler(text="get_a_report")
async def get_doc(call: CallbackQuery):
    print(call.from_user.full_name, call.from_user.id)
    await call.message.edit_text("Сейчас мы вам пришлем анализ индекса потребительских цен за последний месяц")
    await inference()

    photo = r"D:\Code\bot_for_cfo\data\photo\graph.png"
    photo2 = r"D:\Code\bot_for_cfo\data\photo\graph2.png"
    await bot.send_photo(chat_id=call.from_user.id, photo=types.InputFile(photo),
                         caption="На графике представлены изменения цен на товары")
    await asyncio.sleep(1)
    await bot.send_photo(chat_id=call.from_user.id, photo=types.InputFile(photo2),
                         reply_markup=await report_setting(), caption="На графике представлен анализ временного ряда")


@dp.callback_query_handler(text="start_menu")
async def back_to_start_menu(call: CallbackQuery):
    await call.message.answer(f"Приветствую вас, {call.from_user.full_name}!\n\n"
                              f"С помощью данного бота вы сможете регулярно получать отчеты по прогнозированию"
                              f"индекса потребительских цен в текущем месяце и инфляции",
                              reply_markup=await main_keyboard())
