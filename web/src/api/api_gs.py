from fastapi import Depends, HTTPException
from fastapi import APIRouter

import logging

from src.schemas import RowIn, RowResult, RowRequestSingle, RowRequestMany
from src.models import GoogleTable
from src.db import AsyncSession, get_async_session


logger = logging.getLogger(__name__)


api_router = APIRouter()


# Выносим логику записи в отдельную функцию
async def process_row(payload: RowIn, session: AsyncSession) -> RowResult:
    try:
        logger.warning(payload)
        logger.warning('----')
        await GoogleTable.add(
            session=session,
            row_id=payload.row_number,
            sport=payload.sport,
            tournament=payload.tournament,
            match=payload.match,
            date=payload.date,
            time=payload.time,
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


@api_router.post("/add-row", status_code=201)
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


@api_router.post("/add-rows", status_code=201)
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


@api_router.get('/test')
async def test_connect():
    return {'Jry': True}
