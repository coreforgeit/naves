from aiogram import Dispatcher, Router
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import asyncio
import uvloop

from settings import conf
from enums.base import MenuCommand

ENGINE = create_async_engine(url=conf.db_url)



asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
bot = Bot(
    token=conf.token,
    loop=loop,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

main_router = Router()
client_router = Router()
error_router = Router()








async def set_main_menu():
    await bot.set_my_commands([
        BotCommand(command=cmd.command, description=cmd.label)
        for cmd in MenuCommand
    ])
