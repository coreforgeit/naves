import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

import typing as t

from .base import Base
from enums import SPORT_EMOJI


class FcImage(Base):
    __tablename__ = "fc_images"

    url: Mapped[str] = mapped_column(sa.String)
    tg_photo_id: Mapped[str] = mapped_column(sa.String)
    bot_id: Mapped[int] = mapped_column(sa.BigInteger)

    @classmethod
    async def add(cls, session: AsyncSession, url: str, bot_id: int, file_id: str) -> t.Optional[t.Self]:
        """Добавляет строку в кеш"""

        stmt = sa.select(cls).where(cls.url == url)

        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_url(cls, session: AsyncSession, url: str, bot_id: int) -> t.Optional[t.Self]:
        """Возвращает строку по url"""

        stmt = sa.select(cls).where(cls.url == url, cls.bot_id == bot_id)

        result = await session.execute(stmt)
        return result.scalars().first()
