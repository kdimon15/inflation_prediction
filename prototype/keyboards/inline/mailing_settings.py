from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def mailing_setting():
    markup = InlineKeyboardMarkup(row_width=1)
    morning_mailing = InlineKeyboardButton(text="🌅 Присылать утром", callback_data="morning")
    afternoon_mailing = InlineKeyboardButton(text="🌇 Присылать утром", callback_data="afternoon")
    evening_mailing = InlineKeyboardButton(text="🌃 Присылать утром", callback_data="evening")
    back = InlineKeyboardButton(text="⏪️ Вернуться в меню", callback_data="start_menu")
    markup.add(morning_mailing, afternoon_mailing, evening_mailing, back)
    return markup
