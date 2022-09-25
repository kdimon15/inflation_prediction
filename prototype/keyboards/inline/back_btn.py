from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def back_button():
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(back)
    return markup
