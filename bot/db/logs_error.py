from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from sqlalchemy.dialects import postgresql as psql

import sqlalchemy as sa
import typing as t

# from .base import Base, begin_connection
from .base import Base


class LogsError(Base):
    __tablename__ = "logs_error"

    traceback: Mapped[str] = mapped_column(sa.Text, nullable=True)
    message: Mapped[str] = mapped_column(sa.Text, nullable=True)
    comment: Mapped[str] = mapped_column(sa.String, nullable=True)

    @classmethod
    async def add(cls, user_id: int, traceback: str, message: str) -> None:
        query = sa.insert(cls).values(user_id=user_id, traceback=traceback, message=message)

        async with begin_connection() as conn:
            await conn.execute(query)
            await conn.commit()
