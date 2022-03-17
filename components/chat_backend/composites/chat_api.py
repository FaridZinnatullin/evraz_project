from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from components.chat_backend.adapters import database, chat_api
from components.chat_backend.application import services

class Settings:
    db = database.Settings()
    # chat_api = chat_api.Settings()


# class Logger:
#     log.configure(
#         Settings.db.LOGGING_CONFIG,
#         Settings.shop_api.LOGGING_CONFIG,
#     )