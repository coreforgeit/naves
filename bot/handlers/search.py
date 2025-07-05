from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

import models
import keyboards as kb
import utils as ut
from models import User
from settings import conf, log_error
from init import client_router, bot
from enums import CB, UserState, Action, SearchStep, MenuCommand


# выбор спорта
@client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_MATCH.value))
async def search_start(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
    _, value = cb.data.split(':')

    # действия пользователя
    action_button = value
    comment = None

    step_key = 'step'
    current_state = await state.get_state()
    if not current_state:
        await state.set_state(UserState.SEARCH.value)
        await state.update_data(data={step_key: SearchStep.START.value})

    data = await state.get_data()
    step = data.get(step_key)

    enum_step = -1 if value == Action.BACK.value else 1
    next_step = ut.get_adjacent_enum(enum_cls=SearchStep, current_value=step, enum_step=enum_step)
    await state.update_data(data={step_key: next_step})

    if value == Action.BACK.value:
        comment = action_button
        action_button = '🔙 Назад'

    if next_step == SearchStep.SPORT.value:
        if value != Action.BACK.value:
            top_match = bool(int(value)) if value.isdigit() else False
            await state.update_data(data={'top_match': top_match})

            action_button = '🔥 Топ-прогнозы' if top_match else '🔍 Поиск матча'

        sports = await models.GoogleTable.get_unique_sports(session,  only_top=data.get('sport', False))
        text = f'Выбери вид спорта'
        reply_markup = kb.get_sports_kb(sports)

    elif next_step == SearchStep.TOURNAMENT.value:
        if value == Action.BACK.value:
            value = data.get('sport')
        else:
            await state.update_data(data={'sport': value})

        tournaments = await models.GoogleTable.get_tournaments_by_sport(
            session,
            sport=value,
            only_top=data.get('sport', False)
        )
        text = f'Выбери турнир или перейди к ручному поиску'
        reply_markup = kb.get_tournaments_kb(tournaments)

        # await cb.message.edit_text(text=text, reply_markup=kb.get_tournaments_kb(tournaments))

    elif next_step == SearchStep.MATCH.value:
        if value == Action.BACK.value:
            value = data.get('tournament')
        else:
            await state.update_data(data={'tournament': value})

        forecasts = await models.GoogleTable.get_forecast_many(
            session,
            sport=data.get('sport'),
            tournament=value,
            only_top=data.get('sport', False)
        )

        text = f'Выбери матч или перейди к ручному поиску'
        reply_markup = kb.get_match_kb(forecasts)

        # await cb.message.edit_text(text=text, reply_markup=kb.get_match_kb(forecasts))

    elif next_step == SearchStep.RESULT.value:
        forecast = await models.GoogleTable.get_by_id(session, entry_id=int(value))

        await cb.message.edit_reply_markup(reply_markup=None)
        await ut.send_forecast(
            session,
            chat_id=cb.from_user.id,
            forecast=forecast,
        )
        # что нажал пользователь
        await models.LogsUser.add(session=session, user_id=cb.from_user.id, button=forecast.match)
        return
    else:
        text = f'‼️ Произошёл сбой, попробуйте ещё раз /{MenuCommand.START.command}'
        reply_markup = kb.get_back_kb()

    try:
        await cb.message.edit_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        await cb.message.answer(text=text, reply_markup=reply_markup)

    # что нажал пользователь
    await models.LogsUser.add(
        session=session,
        user_id=cb.from_user.id,
        button=action_button,
        comment=comment
    )




# выбор турнира
# @client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_TOURNAMENT.value))
# async def search_tournament(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
#     _, sport = cb.data.split(':')
#
#     if sport == Action.BACK.value:
#         data = await state.get_data()
#         sport = data.get('sport')
#
#     else:
#         await state.set_state(UserState.SEARCH.value)
#         await state.update_data(data={'sport': sport})
#
#     tournaments = await models.GoogleTable.get_tournaments_by_sport(session, sport=sport)
#     text = f'Выбери турнир или перейди к ручному поиску'
#
#     await cb.message.edit_text(text=text, reply_markup=kb.get_tournaments_kb(tournaments))


# выбор статистика
# @client_router.callback_query(lambda cb: cb.data.startswith(CB.SEARCH_GET_RESULT.value))
# async def search_tournament(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
#     _, tournament = cb.data.split(':')
#
#     top_match = True if tournament == Action.TOP.value else False
#
#     data = await state.get_data()
#     forecasts = await models.GoogleTable.get_forecast_many(
#         session,
#         sport=data.get('sport'),
#         tournament=tournament,
#         only_top=top_match
#     )
#
#     await cb.message.edit_reply_markup(reply_markup=None)
#
#     for forecast in forecasts:
#         await ut.send_forecast(
#             session,
#             chat_id=cb.from_user.id,
#             forecast=forecast,
#             top_match=top_match
#         )

