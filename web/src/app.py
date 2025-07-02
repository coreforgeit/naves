from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from starlette import status


import typing as t
import os
import logging


from .schemas import RowIn, RowResult, RowRequestSingle, RowRequestMany
from .db import GoogleTable


logger = logging.getLogger(__name__)

app = FastAPI()


db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_async_engine(db_url, echo=False)
# sessionmaker создает сессии (фабрика)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# dependency для FastAPI
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Выносим логику записи в отдельную функцию
async def process_row(payload: RowIn, session: AsyncSession) -> RowResult:
    try:
        await GoogleTable.add(
            session=session,
            row_id=payload.row_number,
            sport=payload.sport,
            tournament=payload.tournament,
            match=payload.match,
            date=payload.date,
            is_top_match=payload.is_top_match,
            coefficient=payload.coefficient,
            prediction=payload.prediction,
            bet=payload.bet,
            image=payload.image,
            broadcast=payload.broadcast,
        )
        return RowResult(row=payload.row_number, success=True)
    except ValueError as e:
        return RowResult(row=payload.row_number, success=False, error_text=str(e))
    except Exception as e:
        return RowResult(row=payload.row_number, success=False, error_text=f"{e}")


@app.post("/api/add-row", status_code=201)
async def add_row(
    body: RowRequestSingle,
    session: AsyncSession = Depends(get_async_session)
) -> RowResult:
    try:
        # result = await process_row(body.row, session)
        try:
            payload = RowIn.parse_obj(body.row)
            result = await process_row(payload, session)
        except Exception as e:
            err: dict = e.errors()[0]
            e_text = err.get('msg', 'Value error, f')[13:]
            result = RowResult(
                row=body.row.get("row_number"),
                success=False,
                error_text=f"{e_text}"
            )
        return result

    # Если структура данных неверная
    except Exception as e:
        logger.warning(e, exc_info=True)
        HTTPException(
            status_code=422,
            detail=str(e)
    )


@app.post("/api/add-rows", status_code=201)
async def add_rows(
    body: RowRequestMany,
    session: AsyncSession = Depends(get_async_session)
) -> list[RowResult]:
    try:
        results = []

        for item in body.rows:
            try:
                payload = RowIn.parse_obj(item)
            except Exception as e:
                err: dict = e.errors()[0]
                e_text = err.get('msg', 'Value error, f')[13:]
                results.append(RowResult(
                    row=item.get("row_number") if isinstance(item, dict) else None,
                    success=False,
                    error_text=f"{e_text}"
                ))
                continue
            result = await process_row(payload, session)
            results.append(result)
        return results
    except Exception as e:
        # Если структура данных неверная
        logger.warning(e, exc_info=True)
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


# @app.post("/row", status_code=201)
# async def add_row(
#     payload: RowIn,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     logger.warning(f'payload.date: {payload.date}')
#     # Собираем все параметры
#     try:
#         d = {'row': payload.row_number,
#              'success': True/False,
#              'error_text': str
#              }
#         await GoogleTable.add(
#             session=session,
#             row_id=payload.row_number,
#             sport=payload.sport,
#             tournament=payload.tournament,
#             match=payload.match,
#             date=payload.date,
#             is_top_match=payload.is_top_match,
#             coefficient=payload.coefficient,
#             prediction=payload.prediction,
#             bet=payload.bet,
#             image=payload.image,
#             broadcast=payload.broadcast,
#             # row_number=payload.row_number,
#         )
#         return {"detail": "Запись успешно добавлена или обновлена."}
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=str(e)
#         )
#     except Exception as e:
#         logger.warning(e, exc_info=True)
#         raise HTTPException(
#             status_code=500,
#             detail=f"Внутренняя ошибка сервера: {e}"
#         )
