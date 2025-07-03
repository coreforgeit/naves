import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

import typing as t

from .base import Base
from enums import SPORT_EMOJI


class GoogleTable(Base):
    __tablename__ = "google_table"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    sport: Mapped[str] = mapped_column(sa.Text, nullable=True)
    tournament: Mapped[str] = mapped_column(sa.Text, nullable=True)
    match: Mapped[str] = mapped_column(sa.Text, nullable=True)
    date: Mapped[date] = mapped_column(sa.Date, nullable=True)
    is_top_match: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)
    coefficient: Mapped[str] = mapped_column(sa.Text, nullable=True)
    prediction: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bet: Mapped[str] = mapped_column(sa.Text, nullable=True)
    image: Mapped[str] = mapped_column(sa.Text, nullable=True)
    broadcast: Mapped[str] = mapped_column(sa.String, nullable=True)
    # row_number: Mapped[int] = mapped_column(sa.Integer, nullable=True)

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            row_id: int,
            sport: str = None,
            tournament: str = None,
            match: str = None,
            date: datetime = None,
            is_top_match: bool = None,
            coefficient: str = None,
            prediction: str = None,
            bet: str = None,
            image: str = None,
            broadcast: bool = None,
            # row_number: int = None
    ) -> None:
        """Добавляет или обновляет запись в таблице match_rows"""

        now = datetime.now()

        stmt = (
            psql.insert(cls)
            .values(
                id=row_id,
                sport=sport,
                tournament=tournament,
                match=match,
                date=date,
                is_top_match=is_top_match,
                coefficient=coefficient,
                prediction=prediction,
                bet=bet,
                image=image,
                broadcast=broadcast,
                # row_number=row_number,
                # created_at=now,
                # updated_at=now,
            )
            .on_conflict_do_update(
                index_elements=[cls.id],
                set_={
                    "sport": sport,
                    "tournament": tournament,
                    "match": match,
                    "date": date,
                    "is_top_match": is_top_match,
                    "coefficient": coefficient,
                    "prediction": prediction,
                    "bet": bet,
                    "image": image,
                    "broadcast": broadcast,
                    # "row_number": row_number,
                    # "updated_at": now,
                }
            )
        )

        async with session as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_unique_sports(cls, session: AsyncSession) -> list[str]:
        stmt = sa.select(sa.func.distinct(cls.sport)).where(cls.sport.is_not(None))
        result = await session.execute(stmt)
        sports = [row[0] for row in result.fetchall()]
        return sports

    @classmethod
    async def get_tournaments_by_sport(cls, session: AsyncSession, sport: str) -> list[str]:
        today = datetime.now().date()
        stmt = (
            sa.select(sa.func.distinct(cls.tournament))
            .where(
                cls.sport == sport,
                cls.date >= today
            )
        )
        result = await session.execute(stmt)
        tournaments = [row[0] for row in result.fetchall() if row[0]]
        return tournaments

    @classmethod
    async def get_forecast_many(
            cls,
            session: AsyncSession,
            sport: str,
            tournament: str,
            only_top: bool
    ) -> list[t.Self]:
        today = datetime.now().date()
        stmt = sa.select(cls).where(cls.date >= today)

        if only_top:
            stmt = stmt.where(cls.is_top_match.is_(True))
        else:
            stmt = stmt.where(
                cls.sport == sport,
                cls.tournament == tournament
            )

        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def search_by_match(cls, session: AsyncSession, substring: str, sport: str = None) -> list[t.Self]:
        stmt = sa.select(cls).limit(8)

        if substring:
            stmt = stmt.where(sa.func.lower(cls.match).like(f"%{substring.lower()}%"))

        if sport:
            stmt = stmt.where(cls.sport == sport)

        result = await session.execute(stmt)
        return result.scalars().all()
