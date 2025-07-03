import aiohttp
from aiogram.types import BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession


import db
import keyboards as kb
from init import bot
from settings import conf, log_error
from enums import SPORT_EMOJI


# текст прадсказания
def get_forecast_text(forecast: db.GoogleTable) -> str:
    emoji = SPORT_EMOJI.get(forecast.sport.lower(), '')
    data_str = forecast.date.strftime(conf.date_format)
    broadcast = f'📺 Прямая трансляция: <a href="{forecast.broadcast}">Смотреть</a>' if forecast.broadcast else ''
    return (
        f'{emoji} {forecast.tournament}: {forecast.match}\n'
        f'📅 {data_str}\n'
        f'📈 {forecast.coefficient}\n'
        f'🔮 Прогноз: {forecast.prediction}\n'
        f'🎯 Ставка: {forecast.bet}\n'
        f'{broadcast}'
    ).strip()


async def download_photo(url: str) -> BufferedInputFile | None:
    # Скачиваем изображение по ссылке
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            photo_bytes = await resp.read()

    return BufferedInputFile(file=photo_bytes, filename=f'dddd.png')


# отправляет прогноз
async def send_forecast(session: AsyncSession, chat_id: int, forecast: db.GoogleTable, top_match: bool = False) -> None:
    image = await db.FcImage.get_by_url(session, url=forecast.image, bot_id=conf.bot_id)
    if not image:
        photo = await download_photo(forecast.image)
        add_photo = True
    else:
        photo = image.tg_photo_id
        add_photo = False

    text = get_forecast_text(forecast)
    try:
        sent = await bot.send_photo(
            chat_id=chat_id, photo=photo, caption=text, reply_markup=kb.get_forecast_kb(top_match)
        )
        if add_photo:
            await db.FcImage.add(session, url=forecast.image, bot_id=conf.bot_id, file_id=sent.photo[-1].file_id)
    except Exception as e:
        log_error(e)
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb.get_forecast_kb(top_match))
