from aiogram.types import ErrorEvent, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from init import error_router
from settings import log_error, conf
from models import LogsError


if not conf.debug:
    @error_router.errors()
    async def error_handler(ex: ErrorEvent, session: AsyncSession):
        tb, msg = log_error (ex)
        user_id = ex.update.message.from_user.id if ex.update.message else None

        await LogsError.add(session, user_id=user_id, traceback=tb, message=msg)


@error_router.message()
async def free_msg_hnd(msg: Message):
    print(f'free_msg_hnd:\n{msg.content_type}')


# проверяет подписку, в случае удачи пропускает
@error_router.callback_query()
async def free_cb_hnd(cb: CallbackQuery):
    print(f'free_cb_hnd:\n{cb.data}')
