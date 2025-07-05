from fastapi import FastAPI
from src.admin.bot_admin import setup_admin

import logging

from src.api import api_router
from src.auth import AdminAuthMiddleware, auth_router
from src.config import conf

# при отладке в консоль на проде в файл
if conf.debug:
    handler = logging.StreamHandler()
else:
    handler = logging.FileHandler("logs/app.log", encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[handler]
)

logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")
async def create_admin():
    from src.db import AsyncSessionLocal  # импортируй здесь, чтобы избежать циклов
    from src.models import AdminUser
    async with AsyncSessionLocal() as session:
        res = await AdminUser.add_admin_user(session, username=conf.admin_user, password=conf.admin_pass)
        logger.warning(f'res: {res}')

app.add_middleware(AdminAuthMiddleware)

setup_admin(app)

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")
# app.include_router(admin_router, prefix="/admin")
