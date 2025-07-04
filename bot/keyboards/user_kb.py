from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import models
from settings import conf
from enums import CB, Action, SPORT_EMOJI


def get_back_kb(cb: str = CB.COM_START.value, value: str = Action.BACK.value) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{cb}:{value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Поиск матча', callback_data=f'{CB.SEARCH_MATCH.value}:0')
    kb.button(text='🔥 Топ-прогнозы', callback_data=f'{CB.SEARCH_MATCH.value}:1')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_sports_kb(sports: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Поиск', switch_inline_query_current_chat='')

    for sport in sports:
        title = f'{SPORT_EMOJI.get(sport.lower(), '')} {sport}'.strip()
        kb.button(text=title, callback_data=f'{CB.SEARCH_MATCH.value}:{sport}')
    kb.button(text='🔙 Назад', callback_data=f'{CB.COM_START.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_tournaments_kb(tournaments: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Поиск', switch_inline_query_current_chat='')

    for tournament in tournaments:
        kb.button(text=tournament, callback_data=f'{CB.SEARCH_MATCH.value}:{tournament}')
    kb.button(text='🔙 Назад', callback_data=f'{CB.SEARCH_MATCH.value}:{Action.BACK.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_match_kb(match_list: list[models.GoogleTable]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Поиск', switch_inline_query_current_chat='')

    for match in match_list:
        kb.button(text=match.match, callback_data=f'{CB.SEARCH_MATCH.value}:{match.id}')
    kb.button(text='🔙 Назад', callback_data=f'{CB.SEARCH_MATCH.value}:{Action.BACK.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_forecast_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='💰 Сделать ставку', url=conf.bet_url)
    kb.button(text='🔙 Назад', callback_data=f'{CB.SEARCH_MATCH.value}:{Action.BACK.value}')
    return kb.adjust(1).as_markup()