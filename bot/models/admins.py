import logging

from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

import typing as t
import logging

from .base import Base


class AdminUser(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    @classmethod
    async def add_admin_user(cls, session: AsyncSession, username: str, password: str) -> bool:
        # Проверяем, существует ли такой пользователь
        stmt = sa.select(cls).where(cls.username == username)
        result = await session.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            return False  # Пользователь уже существует

        # Хэшируем пароль
        hashed_password = bcrypt.hash(password)

        # Создаём пользователя
        stmt = sa.insert(cls).values(
            username=username,
            hashed_password=hashed_password,
        )
        await session.execute(stmt)
        await session.commit()
        return True  # Пользователь успешно добавлен

    @classmethod
    async def authenticate_user(cls, session: AsyncSession, username: str, password: str) -> t.Self | None:
        # input_password = bcrypt.hash(password)

        stmt = sa.select(cls).where(cls.username == username)
        result = await session.execute(stmt)
        user = result.scalars().first()
        # logging.warning(f'user {user}')
        # logging.warning(f'bcrypt {bcrypt.verify(password, user.hashed_password)}')
        if not user:
            return None
        elif bcrypt.verify(password, user.hashed_password):
            return user
        return None
