from typing import List, Optional

from classic.sql_storage import BaseRepository
from classic.components import component
from components.chat_backend.application import interfaces
from components.chat_backend.application.dataclasses import User, ChatUser, Chat, ChatMessage, ChatSuperusers, \
    ChatBlackList
from sqlalchemy.sql import select, and_


@component
class ChatsRepo(BaseRepository, interfaces.ChatRepo):
    def get_all_messages(self, id_chat: int) -> List[ChatMessage]:
        if id_chat:
            query = select(Chat).where(Chat.id == id_chat)
            chat = self.session.execute(query).scalars().all()
            return chat.messages

    def get_all_users(self, id_chat: int) -> List[ChatUser]:
        if id_chat:
            query = select(Chat).where(Chat.id == id_chat).one()
            chat = self.session.execute(query).scalars().all()
            return chat.users

    def get_all_chats_by_user(self, id_user: int) -> List[Chat]:
        if id_user:
            chat_list = []
            chatusers_query = select(ChatUser).where(ChatUser.user.id == id_user)
            chatusers = self.session.execute(chatusers_query)
            for chatuser in chatusers:
                chat_list.append(chatuser.chat)

            return chat_list
