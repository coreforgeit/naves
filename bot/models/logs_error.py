from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

import sqlalchemy as sa
import typing as t

from .base import Base


class LogsError(Base):
    __tablename__ = "logs_error"

    traceback: Mapped[str] = mapped_column(sa.Text, nullable=True)
    message: Mapped[str] = mapped_column(sa.Text, nullable=True)
    comment: Mapped[str] = mapped_column(sa.String, nullable=True)

    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, traceback: str, message: str) -> None:
        stmt = sa.insert(cls).values(user_id=user_id, traceback=traceback, message=message)

        async with session as conn:
            await conn.execute(stmt)
            await conn.commit()
