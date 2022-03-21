from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from components.chat_backend.adapters import database, chat_api
from components.chat_backend.application import services


class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    # database.metadata.drop_all(engine)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine)

    chats_repo = database.repositories.ChatRepo(context=context)
    chats_user_repo = database.repositories.ChatUserRepo(context=context)
    user_repo = database.repositories.UserRepo(context=context)
    chat_messages_repo = database.repositories.MessageRepo(context=context)


class Application:
    chat_manager = services.ChatManager(
        chats_repo=DB.chats_repo,
        chats_user_repo=DB.chats_user_repo,
        user_repo=DB.user_repo,
        chat_messages_repo=DB.chat_messages_repo,
    )

    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    allow_origins = Settings.chat_api.ALLOW_ORIGINS


class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    allow_origins=Application.allow_origins,
    chat_manager=Application.chat_manager,

)

if __name__ == '__main__':
    from wsgiref import simple_server

    with simple_server.make_server('', 8000, app=app) as server:
        server.serve_forever()
