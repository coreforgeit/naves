import logging

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, date, time, timedelta

from src.config import conf


class RowIn(BaseModel):
    id: int
    sport: Optional[str] = None
    tournament: Optional[str] = None
    match: Optional[str] = None
    date_match: Optional[date] = None
    time_match: Optional[time] = None
    is_top_match: Optional[bool] = None
    coefficient: Optional[str] = None
    prediction: Optional[str] = None
    bet: Optional[str] = None
    image: Optional[str] = None
    broadcast: Optional[str] = None
    row_number: Optional[int] = None

    @field_validator('date_match', mode='before')
    def parse_date(cls, v):
        try:
            t = datetime.strptime(v, conf.date_format)
            return t.date()
        except Exception:
            raise ValueError("Некорректный формат даты")

    @field_validator('time_match', mode='before')
    def parse_time(cls, v):
        try:
            t = datetime.strptime(v, conf.time_format) - timedelta(hours=3)  # приводим к utc

            return t.time()
        except Exception:
            raise ValueError("Некорректный формат времени")

    @field_validator('is_top_match', mode='before')
    def parse_bool(cls, v):
        if v is None:
            return None
        if isinstance(v, bool):
            return v
        s = str(v).strip().lower()
        return s == "да"

        # raise ValueError('Поле должно содержать только "да" или "нет"')

    @field_validator('image', 'broadcast', mode='before')
    def parse_url(cls, v):
        try:
            v = str(v).strip()
            return v if v.startswith('https://') else None
        except Exception as e:
            raise ValueError(f'{e}')

    @field_validator('sport', 'tournament', 'match', 'coefficient', 'prediction', 'bet', mode='before')
    def empty_string_to_none(cls, v):
        return v if v != "" else None

    model_config = {
        "str_strip_whitespace": True
    }


class RowResult(BaseModel):
    row: Optional[int]
    success: bool
    error_text: Optional[str] = None


class RowRequestSingle(BaseModel):
    row: dict


class RowRequestMany(BaseModel):
    # rows: list[RowIn]
    rows: list[dict]
