import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


# from .base import Base, begin_connection
from .base import Base


class GoogleTable(Base):
    __tablename__ = "google_table"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    sport: Mapped[str] = mapped_column(sa.Text, nullable=True)
    tournament: Mapped[str] = mapped_column(sa.Text, nullable=True)
    match: Mapped[str] = mapped_column(sa.Text, nullable=True)
    date: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)
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
