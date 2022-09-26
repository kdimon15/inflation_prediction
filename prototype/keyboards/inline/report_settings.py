from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def report_setting():
    markup = InlineKeyboardMarkup()
    setting = InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
    back = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(setting)
    markup.add(back)
    return markup
