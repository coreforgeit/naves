from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

import db
import keyboards as kb
import utils as ut
from db import User
from settings import conf, log_error
from init import main_router, bot
# from enums import CB, MenuCommand


@main_router.message(CommandStart())
async def com_start(msg: Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    # await db.User.add(
    #     session=session,
    #     user_id=msg.from_user.id,
    #     full_name=msg.from_user.full_name,
    #     username=msg.from_user.username,
    # )

    await msg.answer('На месте')

