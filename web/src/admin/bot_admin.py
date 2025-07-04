# src/admin/admin.py

from sqladmin import Admin, ModelView
from src.models import GoogleTable, User
from src.db import engine  # твой engine


def setup_admin(app):
    admin = Admin(app, engine)

    class GoogleTableAdmin(ModelView, model=GoogleTable):
        column_list = [
            GoogleTable.id, GoogleTable.sport, GoogleTable.tournament, GoogleTable.match, GoogleTable.is_top_match
        ]

    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.full_name, User.username, User.created_at, User.updated_at]
        form_excluded_columns = [User.created_at, User.updated_at]
        column_searchable_list = [User.id, User.full_name, User.username]
        can_edit = [User.full_name]
        column_labels = {
            User.id: 'ID',
            User.full_name: 'Имя',
            User.username: 'Юзернейм',
            User.created_at: 'Первый визит',
            User.updated_at: 'Последний визит',
        }

        name = "Пользователь"
        name_plural = "Пользователи"

    admin.add_view(GoogleTableAdmin)
    admin.add_view(UserAdmin)



