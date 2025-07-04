from fastapi import Request, HTTPException, status, APIRouter, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.models import AdminUser, AdminSession
from src.db import AsyncSessionLocal

import secrets
import logging


templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
auth_router = APIRouter()


class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Проверяем только /admin
        if request.url.path.startswith("/admin"):
            username = request.cookies.get("username")
            token = request.cookies.get("session_token")
            logging.warning(f'username: {username}')
            logging.warning(f'token: {token}')

            if not username or not token:
                return RedirectResponse(url="/auth/login", status_code=302)

            async with AsyncSessionLocal() as session:
                check = await AdminSession.check(session, username=username, session_token=token)
            logging.warning(f'check: {check}')
            if check:
                return await call_next(request)

            return RedirectResponse(url='/auth/login', status_code=302)

        return await call_next(request)


@auth_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with AsyncSessionLocal() as session:
        user = await AdminUser.authenticate_user(
            session,
            username=username,
            password=password
        )

        if not user:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

        token = secrets.token_urlsafe(32)

        await AdminSession.add(session, username=username, session_token=token)

    response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    response.set_cookie("username", username, httponly=True, max_age=60 * 60 * 24 * 365 * 10)
    response.set_cookie("session_token", token, httponly=True, max_age=60 * 60 * 24 * 365 * 10)
    return response


@auth_router.post("/logout")
async def logout(request: Request):
    username = request.cookies.get("admin_username")
    token = request.cookies.get("admin_token")
    if username and token:
        async with AsyncSessionLocal() as session:
            # Удаляем только конкретную сессию пользователя
            await AdminSession.delete(session, username=username, session_token=token)

    # Удаляем куки (ставим пустое значение и max_age=0)
    response = RedirectResponse(url="auth/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("admin_username")
    response.delete_cookie("admin_token")
    return response
