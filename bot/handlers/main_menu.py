from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
from aiogram.enums.content_type import ContentType
from sqlalchemy.ext.asyncio import AsyncSession

import models
import keyboards as kb
import utils as ut
from models import User
from settings import conf, log_error
from init import main_router, bot
from enums import CB, MenuCommand


@main_router.message(CommandStart())
async def com_start(msg: Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    await models.User.add(
        session=session,
        user_id=msg.from_user.id,
        full_name=msg.from_user.full_name,
        username=msg.from_user.username,
    )

    await msg.answer('<b>🔹 Главное меню </b>', reply_markup=kb.get_main_menu_kb())

    await models.LogsUser.add(session=session, user_id=msg.from_user.id, button=msg.text)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.COM_START.value))
async def search_start(cb: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    try:
        await cb.message.edit_text('<b>🔹 Главное меню </b>', reply_markup=kb.get_main_menu_kb())
    except:
        await cb.message.answer('<b>🔹 Главное меню </b>', reply_markup=kb.get_main_menu_kb())

    await models.LogsUser.add(session=session, user_id=cb.from_user.id, button='🔙 Назад', comment='Главное меню')

