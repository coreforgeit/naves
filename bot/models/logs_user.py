from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

import sqlalchemy as sa
import typing as t

# from .base import Base, begin_connection
from .base import Base


class LogsUser(Base):
    __tablename__ = "logs_users"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    button: Mapped[str] = mapped_column(sa.String)
    comment: Mapped[str] = mapped_column(sa.String, nullable=True)

    user = relationship("User", backref="logs")


    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, button: str, comment: str = None) -> None:
        stmt = sa.insert(cls).values(user_id=user_id, button=button)

        if comment:
            stmt = stmt.values(comment=comment[:255])

        async with session as conn:
            await conn.execute(stmt)
            await conn.commit()
