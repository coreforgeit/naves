from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from settings import conf
# from enums import CB, TariffType, UserStatusFSM


# Кнопки подписаться на канал
def get_subscribe_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🏃‍➡️ ПОДПИСАТЬСЯ', url=conf.channel_link)
    kb.button(text='🎯 Я ПОДПИСАН(А)', callback_data=f'{CB.CHECK_SUBSCRIBE.value}')
    return kb.adjust(1).as_markup()
