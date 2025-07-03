from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession


import db
import keyboards as kb
import utils as ut
from db import User
from settings import conf, log_error
from init import client_router, bot
from enums import CB, UserState, Action


@client_router.inline_query()
async def inline_search_handler(inline_query: InlineQuery, state: FSMContext, session: AsyncSession):
    # Получаем поисковый запрос пользователя
    query = inline_query.query.strip().lower()

    data = await state.get_data()
    sport = data.get('sport')

    # Здесь логика поиска (например, по ключевым словам)
    forecasts = await db.GoogleTable.search_by_match(session, substring=query, sport=sport)
    # если нет результатов, то возвращает все
    # if not forecasts:
    #     forecasts = await db.GoogleTable.search_by_match(session, substring='')

    results = []
    if forecasts:
        for forecast in forecasts:
            text = ut.get_forecast_text(forecast)
            results.append(
                InlineQueryResultArticle(
                    id=str(forecast.id),
                    title=forecast.match,
                    input_message_content=InputTextMessageContent(
                        message_text=text
                    ),
                    description=forecast.date.strftime(conf.date_format),
                )
            )
    # Отправляем результаты пользователю
    await inline_query.answer(results, cache_time=1)


# @client_router.chosen_inline_result()
# @client_router.chosen_inline_result(StateFilter(UserState.SEARCH.value))
# async def handle_chosen_inline_result(cq: ChosenInlineResult, state: FSMContext, session: AsyncSession):
#     print(f'@client_router.chosen_inline_result(): {cq.query}')
#
#
# @client_router.message()
# @client_router.message(StateFilter(UserState.SEARCH.value))
# async def handle_chosen_inline_result(msg: Message, state: FSMContext, session: AsyncSession):
#     if msg.text.isdigit():
#         await msg.delete()
#
#         forecast_id = id(msg.text)
#         forecast = await db.GoogleTable.get_by_id(session, entry_id=forecast_id)
#         await ut.send_forecast(
#             session=session,
#             chat_id=msg.chat.id,
#             forecast=forecast
#         )

    # else:
    #     print(f'@client_router.message(): {msg.text}')

