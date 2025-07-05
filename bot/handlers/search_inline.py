from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, ChosenInlineResult, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


import models
import keyboards as kb
import utils as ut
from models import User
from settings import conf, log_error
from init import client_router, bot
from enums import CB, UserState, Action


@client_router.inline_query()
async def inline_search_handler(inline_query: InlineQuery, state: FSMContext, session: AsyncSession):
    # Получаем поисковый запрос пользователя
    query = inline_query.query.strip().lower()

    data = await state.get_data()
    sport = data.get('sport')
    tournament = data.get('tournament')

    # Здесь логика поиска (например, по ключевым словам)
    forecasts = await models.GoogleTable.search_by_match(session, substring=query, sport=sport, tournament=tournament)
    # если нет результатов, то возвращает все
    if not forecasts:
        forecasts = await models.GoogleTable.search_by_match(session, substring='')

    results = []
    if forecasts:
        for forecast in forecasts:
            text = ut.get_forecast_text(forecast)
            results.append(
                InlineQueryResultArticle(
                    # id=str(forecast.id),
                    id=str(uuid4()),
                    title=forecast.match,
                    input_message_content=InputTextMessageContent(
                        message_text=text
                    ),
                    description=forecast.date.strftime(conf.date_format),
                )
            )
    # Отправляем результаты пользователю
    await inline_query.answer(results, cache_time=1)
