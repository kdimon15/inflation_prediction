from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def main_keyboard():
    markup = InlineKeyboardMarkup()
    get_report = InlineKeyboardButton(text="📝 Получить отчет", callback_data="get_a_report")
    info = InlineKeyboardButton(text="🌐 О проекте", callback_data="help")
    markup.row(get_report, info)
    return markup
