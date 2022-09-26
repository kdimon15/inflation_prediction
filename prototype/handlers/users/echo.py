from aiogram import types

from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    print(message.from_user.full_name, message.from_user.id)
    await message.answer(message.text)
