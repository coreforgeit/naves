from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import models
from init import ENGINE

begin_connection = sessionmaker(bind=ENGINE, class_=AsyncSession, expire_on_commit=False)


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with begin_connection() as session:
            data['session'] = session
            return await handler(event, data)


class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id:
            session = data.get('session')
            if session is not None:
                user = await models.User.get_by_id(entry_id=user_id, session=session)
                if user and getattr(user, "is_ban", False):
                    text = '❌ Вам закрыт доступ'
                    if isinstance(event, Message):
                        await event.answer(text)
                    else:
                        await event.message.answer(text)
                    return  # Прерываем цепочку

        return await handler(event, data)