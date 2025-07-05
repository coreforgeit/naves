import typing as t
import sqlalchemy as sa
import os

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


METADATA = sa.MetaData ()


async def init_models(engin):
    async with engin.begin () as conn:
        await conn.run_sync (METADATA.drop_all)
        await conn.run_sync (METADATA.create_all)


class Base(DeclarativeBase):
    metadata = METADATA

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(), default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now())

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"

    @classmethod
    async def get_all(cls, session: AsyncSession) -> t.Optional[list[t.Self]]:
        """Возвращает строку по id"""

        # query = sa.select(cls).where(cls.is_active == True)
        query = sa.select(cls)

        async with session as conn:
            result = await conn.execute(query)

        return result.scalars().all()
        # return result.all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, entry_id: int) -> t.Optional[t.Self]:
        """Возвращает строку по id"""

        query = sa.select(cls).where(cls.id == entry_id)

        async with session as conn:
            result = await conn.execute(query)

        return result.scalars().first()
