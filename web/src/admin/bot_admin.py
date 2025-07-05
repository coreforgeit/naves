# src/admin/admin.py

from sqladmin import Admin, ModelView
from src.models import GoogleTable, User, LogsUser, LogsError
from src.db import engine  # твой engine


def setup_admin(app):
    admin = Admin(app, engine)

    class GoogleTableAdmin(ModelView, model=GoogleTable):
        column_list = [
            GoogleTable.id, GoogleTable.sport, GoogleTable.tournament, GoogleTable.match, GoogleTable.is_top_match
        ]
        name = "Прогноз"
        name_plural = "Прогнозы"

    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.full_name, User.username, User.is_ban, User.created_at, User.updated_at]
        # form_excluded_columns = [User.created_at, User.updated_at]
        column_searchable_list = [User.id, User.full_name, User.username]
        # can_edit = [User.is_ban]
        column_labels = {
            User.id: 'ID',
            User.full_name: 'Имя',
            User.username: 'Юзернейм',
            User.is_ban: 'Заблокирован',
            User.created_at: 'Первый визит',
            User.updated_at: 'Последний визит',
        }

        name = "Пользователь"
        name_plural = "Пользователи"

    class LogsUserAdmin(ModelView, model=LogsUser):
        name = "Действие пользователя"
        name_plural = "Действия пользователей"

        column_list = [
            LogsUser.button,
            LogsUser.comment,
            LogsUser.user,
        ]

        column_labels = {
            LogsUser.button: "Кнопка",
            LogsUser.comment: "Комментарий",
            LogsUser.user: "Имя пользователя",
        }

        # По желанию: можно добавить поиск и фильтры
        column_searchable_list = [LogsUser.button, LogsUser.comment]

    class LogsErrorAdmin(ModelView, model=LogsError):
        name = "Ошибка"
        name_plural = "Ошибки"

        column_list = [
            LogsError.message,
            LogsError.traceback,
            LogsError.comment,
        ]

    admin.add_view(GoogleTableAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(LogsUserAdmin)
    admin.add_view(LogsErrorAdmin)



