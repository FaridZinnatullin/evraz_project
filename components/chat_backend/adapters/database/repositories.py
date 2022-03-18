from typing import List, Optional

from classic.sql_storage import BaseRepository
from classic.components import component
from components.chat_backend.application import interfaces
from components.chat_backend.application.dataclasses import User, ChatUser, Chat, ChatMessage
from sqlalchemy.sql import select, and_


@component
class ChatRepo(BaseRepository, interfaces.ChatRepo):

    def get_all_messages(self, id_chat: int) -> List[ChatMessage]:
        query = select(Chat).where(Chat.id == id_chat)
        chat = self.session.execute(query).scalars().all()
        return chat.messages

    def get_all_users(self, id_chat: int) -> List[ChatUser]:

        query = select(Chat).where(Chat.id == id_chat).one()
        chat = self.session.execute(query).scalars().all()
        return chat.users

    def get_chat_by_tmp_id(self, tmp_id: int) -> Chat:
        query = select(Chat).where(Chat.tmp_id == tmp_id)
        chat = self.session.execute(query).scalars().one_or_none()
        return chat

    # def get_all_chats_by_user_id(self, id_user: int) -> List[Chat]:
    #     if id_user:
    #         chat_list = []
    #         chatusers_query = select(ChatUser).where(ChatUser.user.id == id_user)
    #         chatusers = self.session.execute(chatusers_query)
    #         for chatuser in chatusers:
    #             chat_list.append(chatuser.chat)
    #
    #         return chat_list

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()

    def remove(self, chat: Chat):
        pass

    def get_info(self, chat: Chat):
        pass

    def get(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.id == chat_id)
        chat = self.session.execute(query).scalars().first()
        return chat


@component
class UserRepo(BaseRepository, interfaces.UserRepo):

    def get(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()


    # зачем?

    def get_or_create(self, id_: Optional[int]) -> User:
        ...


@component
class ChatUserRepo(BaseRepository, interfaces.ChatUserRepo):

    def add(self, chatuser: ChatUser):
        self.session.add(chatuser)
        self.session.flush()

    def get(self, chatuser_id: int):
        query = select(ChatUser).where(User.id == chatuser_id)
        return self.session.execute(query).scalars().one_or_none()

@component
class MessageRepo(BaseRepository, interfaces.MessageRepo):

    def add(self, message: ChatMessage):
        ...


# @component
# # class ChatBlackListRepo(BaseRepository, interfaces.ChatBlackListRepo):
# #
# #     def add(self, blacklist: ChatBlackList):
# #         ...
# #
# #     def get_users(self, blacklist: ChatBlackList) -> List[User]:
# #         ...
# #
# #     def clean(self, blacklist: ChatBlackList):
# #         ...
# #
# #
# # @component
# # class ChatSuperusersRepo(BaseRepository, interfaces.ChatSuperusersRepo):
# #
# #     def add(self, superusers: ChatSuperusers):
# #         ...
# #
# #     def get_users(self, superusers: ChatSuperusers) -> List[User]:
# #         ...
# #
# #     def clean(self, superusers: ChatSuperusers):
# #         ...
