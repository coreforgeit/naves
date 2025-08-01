import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date, time, timedelta

import typing as t

from .base import Base


class GoogleTable(Base):
    __tablename__ = "google_table"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    sport: Mapped[str] = mapped_column(sa.Text, nullable=True)
    tournament: Mapped[str] = mapped_column(sa.Text, nullable=True)
    match: Mapped[str] = mapped_column(sa.Text, nullable=True)
    date: Mapped[date] = mapped_column(sa.Date, nullable=True)
    time: Mapped[time] = mapped_column(sa.Time, nullable=True)
    is_top_match: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)
    coefficient: Mapped[str] = mapped_column(sa.Text, nullable=True)
    prediction: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bet: Mapped[str] = mapped_column(sa.Text, nullable=True)
    image: Mapped[str] = mapped_column(sa.Text, nullable=True)
    broadcast: Mapped[str] = mapped_column(sa.String, nullable=True)
    # row_number: Mapped[int] = mapped_column(sa.Integer, nullable=True)

    def msk_time(self):
        # Для примера возьмём сегодняшнюю дату или дату из self.date, если она есть
        base_date = self.date or datetime.today().date()
        dt = datetime.combine(base_date, self.time)  # объединяем дату и время в datetime
        dt_plus_3 = dt + timedelta(hours=3)          # прибавляем 3 часа
        return dt_plus_3.time()

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            row_id: int,
            sport: str = None,
            tournament: str = None,
            match: str = None,
            date: date = None,
            time: time = None,
            is_top_match: bool = None,
            coefficient: str = None,
            prediction: str = None,
            bet: str = None,
            image: str = None,
            broadcast: bool = None,
            # row_number: int = None
    ) -> None:
        """Добавляет или обновляет запись в таблице match_rows"""
        stmt = (
            psql.insert(cls)
            .values(
                id=row_id,
                sport=sport,
                tournament=tournament,
                match=match,
                date=date,
                time=time,
                is_top_match=is_top_match,
                coefficient=coefficient,
                prediction=prediction,
                bet=bet,
                image=image,
                broadcast=broadcast,
            )
            .on_conflict_do_update(
                index_elements=[cls.id],
                set_={
                    "sport": sport,
                    "tournament": tournament,
                    "match": match,
                    "date": date,
                    "time": time,
                    "is_top_match": is_top_match,
                    "coefficient": coefficient,
                    "prediction": prediction,
                    "bet": bet,
                    "image": image,
                    "broadcast": broadcast,
                }
            )
        )

        async with session as conn:
            await conn.execute(stmt)
            await conn.commit()

    @classmethod
    async def get_unique_sports(cls, session: AsyncSession) -> list[str]:
        stmt = sa.select(sa.func.distinct(cls.sport)).where(cls.sport.is_not(None))

        # if only_top:
        #     stmt = stmt.where(cls.is_top_match.is_(True))

        result = await session.execute(stmt)
        sports = [row[0] for row in result.fetchall()]
        return sports

    @classmethod
    async def get_tournaments_by_sport(cls, session: AsyncSession, sport: str, only_top: bool) -> list[str]:
        now = datetime.now()
        stmt = (
            sa.select(sa.func.distinct(cls.tournament))
            .where(
                cls.sport == sport,
                cls.date >= now.date(),
                cls.time >= now.time(),
            )
        )

        if only_top:
            stmt = stmt.where(cls.is_top_match.is_(True))

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
        now = datetime.now()

        stmt = sa.select(cls).where(
            cls.date >= now.date(),
            cls.time >= now.time(),
        )

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
    async def search_by_match(
            cls, session: AsyncSession, substring: str, sport: str = None, tournament: str = None
    ) -> list[t.Self]:
        now = datetime.now()

        stmt = sa.select(cls).where(
            cls.date >= now.date(),
            cls.time >= now.time(),
        ).limit(8)

        if substring:
            stmt = stmt.where(sa.func.lower(cls.match).like(f"%{substring.lower()}%"))

        if sport:
            stmt = stmt.where(cls.sport == sport)

        if tournament:
            stmt = stmt.where(cls.tournament == tournament)

        result = await session.execute(stmt)
        return result.scalars().all()
