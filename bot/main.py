import asyncio
import logging
import sys

from aiogram import Dispatcher
from datetime import datetime

import models
from init import set_main_menu, bot, ENGINE, DBSessionMiddleware
from settings import conf, log_error
from models.base import init_models
from handlers.main_menu import main_router
from handlers import client_router
from handlers.exceptions import error_router


dp = Dispatcher()
dp.message.middleware(DBSessionMiddleware())
dp.callback_query.middleware(DBSessionMiddleware())
dp.inline_query.middleware(DBSessionMiddleware())


async def main() -> None:
    await init_models(ENGINE)
    await set_main_menu()

    dp.include_router(main_router)
    dp.include_router(client_router)
    dp.include_router(error_router)
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if conf.debug:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', wt=False)
    asyncio.run(main())
