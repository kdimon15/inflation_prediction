from aiogram.types import CallbackQuery

from keyboards.inline.back_btn import back_button
from loader import dp


@dp.callback_query_handler(text="help")
async def get_info(call: CallbackQuery):
    print(call.from_user.full_name, call.from_user.id)
    await call.message.edit_text("<b>Постановка задачи</b>\n\n"
                                 "На основе открытых микроданных о потребительских ценах, собранных посредством\n"
                                 "веб-скрейпинга интернет-магазинов Московской области (Московского региона),\n"
                                 "создать модель наукастинга на базе методов машинного обучения, позволяющую\n"
                                 "формировать краткосрочный (на горизонте 1-2 месяцев) прогноз месячного ИПЦ в\n"
                                 "режиме реального времени.\n\n"
                                 "<b>Решение</b>\n\n"
                                 "Решение кейса представляет собой прототип модели наукастинга, которая позволит"
                                 "прогнозировать ИПЦ на краткосрочном горизонте, используя высокочастотные"
                                 "(ежедневные) данные, полученные в ходе"
                                 "мониторинга цен на товары и услуги в онлайн-магазинах\n\n"
                                 "<b>Решение на GitHub - https://github.com/kdimon15/inflation_prediction</b>",
                                 reply_markup=await back_button())
