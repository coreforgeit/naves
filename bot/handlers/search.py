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
    next_step = None

    top_match = True if value == Action.TOP.value else False

    step_key = 'step'
    current_state = await state.get_state()

    if value == Action.TOP.value:
        next_step = SearchStep.MATCH.value
        await state.set_state(UserState.SEARCH.value)
        await state.update_data(data={'top_match': True})
        action_button = '🔥 Топ-прогнозы'

    elif not current_state:
        await state.set_state(UserState.SEARCH.value)
        next_step = SearchStep.SPORT.value

    data = await state.get_data()
    print(data)

    if not next_step:
        step = data.get(step_key)
        enum_step = -1 if value == Action.BACK.value else 1
        next_step = ut.get_adjacent_enum(enum_cls=SearchStep, current_value=step, enum_step=enum_step)

    await state.update_data(data={step_key: next_step})

    print(f'next_step: {next_step}')
    print(f'top_match: {top_match}')

    if value == Action.BACK.value:
        comment = action_button
        action_button = '🔙 Назад'

    if next_step == SearchStep.SPORT.value:
        if value != Action.BACK.value:
            action_button = '🔍 Поиск матча'

        sports = await models.GoogleTable.get_unique_sports(session)
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

        top_match = data.get('top_match', False)
        print(f'top_match 2: {top_match}')
        forecasts = await models.GoogleTable.get_forecast_many(
            session,
            sport=data.get('sport'),
            tournament=value,
            only_top=top_match
        )

        text = f'Выбери матч или перейди к ручному поиску'
        reply_markup = kb.get_match_kb(match_list=forecasts, is_top=top_match)

    elif next_step == SearchStep.RESULT.value:
        forecast = await models.GoogleTable.get_by_id(session, entry_id=int(value))

        top_match = data.get('top_match', False)
        if top_match:
            comment = '🔥 Топ-прогнозы'

        await cb.message.edit_reply_markup(reply_markup=None)
        await ut.send_forecast(
            session,
            chat_id=cb.from_user.id,
            forecast=forecast,
            is_top=top_match
        )
        # что нажал пользователь
        await models.LogsUser.add(session=session, user_id=cb.from_user.id, button=forecast.match, comment=comment)
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
