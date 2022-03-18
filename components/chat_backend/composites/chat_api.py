from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from components.chat_backend.adapters import database, chat_api
from components.chat_backend.application import services


class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()


# class Logger:
#     log.configure(
#         Settings.db.LOGGING_CONFIG,
#         Settings.shop_api.LOGGING_CONFIG,
#     )


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    # database.metadata.drop_all(engine)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine)

    chat_repo = database.repositories.ChatRepo(context=context)
    chat_user_repo = database.repositories.ChatUserRepo(context=context)
    user_repo = database.repositories.UserRepo(context=context)
    # chat_blacklist_repo = database.repositories.ChatBlackListRepo(context=context)
    # chat_superusers_repo = database.repositories.ChatSuperusersRepo(context=context)

    # products_repo = database.repositories.ProductsRepo(context=context)
    # carts_repo = database.repositories.CartsRepo(context=context)
    # orders_repo = database.repositories.OrdersRepo(context=context)


# class MailSending:
#     sender = mail_sending.FileMailSender()


class Application:
    # chats_repo: interfaces.ChatRepo
    # user_repo: interfaces.UserRepo
    # chat_blacklist_repo: interfaces.ChatBlackListRepo
    # chat_superusers_repo: interfaces.ChatSuperusersRepo
    chat_manager = services.ChatManager(
        chats_repo=DB.chat_repo,
        chats_user_repo=DB.chat_user_repo,
        user_repo=DB.user_repo,
    )
    # orders = services.Orders(
    #     orders_repo=DB.orders_repo,
    #     mail_sender=MailSending.sender,
    # )
    # customers = services.Customers(customers_repo=DB.customers_repo)

    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    allow_origins = Settings.chat_api.ALLOW_ORIGINS


class Aspects:
    services.join_points.join(DB.context)
    chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    allow_origins=Application.allow_origins,
    chat_manager=Application.chat_manager,
    # orders=Application.orders,
    # customers=Application.customers,
)

if __name__ == '__main__':
    from wsgiref import simple_server

    with simple_server.make_server('', 8000, app=app) as server:
        server.serve_forever()