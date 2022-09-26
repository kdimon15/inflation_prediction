from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.main_menu import main_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    print(message.from_user.full_name, message.from_user.id)
    await message.answer(f"Приветствую вас, {message.from_user.full_name}!\n\n"
                         f"С помощью данного бота вы сможете регулярно получать отчеты по прогнозированию"
                         f"индекса потребительских цен в текущем месяце и инфляции", reply_markup=await main_keyboard())
