from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

import typing as t

from .base import Base


class AdminSession(Base):
    __tablename__ = "admin_sessions"

    username: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    session_token: Mapped[str] = mapped_column(sa.String(128), nullable=False)

    @classmethod
    async def add(cls, session: AsyncSession, username: str, session_token: str) -> None:
        # Создаём пользователя
        stmt = sa.insert(cls).values(
            username=username,
            session_token=session_token,
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def check(cls, session: AsyncSession, username: str, session_token: str) -> t.Self | None:
        stmt = sa.select(cls).where(cls.username == username, cls.session_token == session_token)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def delete(cls, session: AsyncSession, username: str, session_token: str) -> None:
        stmt = sa.delete(cls).where(cls.username == username, cls.session_token == session_token)
        await session.execute(stmt)
        await session.commit()

