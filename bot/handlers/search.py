from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

import db
import keyboards as kb
import utils as ut
from db import User
from settings import conf, log_error
from init import client_router, bot
from enums import CB, UserState, Action


# выбор спорта
@client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_START.value))
async def search_start(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
    sports = await db.GoogleTable.get_unique_sports(session)
    text = f'Выбери вид спорта'
    await cb.message.edit_text(text=text, reply_markup=kb.get_sports_kb(sports))


# выбор турнира
@client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_TOURNAMENT.value))
async def search_tournament(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
    _, sport = cb.data.split(':')

    if sport == Action.BACK.value:
        data = await state.get_data()
        sport = data.get('sport')

    else:
        await state.set_state(UserState.SEARCH.value)
        await state.update_data(data={'sport': sport})

    tournaments = await db.GoogleTable.get_tournaments_by_sport(session, sport=sport)
    text = f'Выбери турнир или перейди к ручному поиску'

    await cb.message.edit_text(text=text, reply_markup=kb.get_tournaments_kb(tournaments))


# выбор статистика
@client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_GET_RESULT.value))
async def search_tournament(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
    _, tournament = cb.data.split(':')

    top_match = True if tournament == Action.TOP.value else False

    data = await state.get_data()
    forecasts = await db.GoogleTable.get_forecast_many(
        session,
        sport=data.get('sport'),
        tournament=tournament,
        only_top=top_match
    )

    await cb.message.edit_reply_markup(reply_markup=None)

    for forecast in forecasts:
        await ut.send_forecast(
            session,
            chat_id=cb.from_user.id,
            forecast=forecast,
            top_match=top_match
        )

