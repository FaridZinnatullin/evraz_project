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
        query = select(ChatUser).where(ChatUser.chat.id == id_chat)
        chat = self.session.execute(query).scalars().all()
        return chat.users

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()
        return chat


    def remove(self, chat: Chat):
        self.session.delete(chat)

    def get_info(self, chat: Chat):
        pass

    def get(self, chat_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.id == chat_id)
        chat = self.session.execute(query).scalars().first()
        return chat

    def check_permission_member(self, user_id: int, chat_id: int):
        query = select(ChatUser).where(and_(ChatUser.chat_id == chat_id, ChatUser.user_id == user_id))
        chatuser = self.session.execute(query).scalars().first()
        if chatuser:
            if not chatuser.banned:
                return True
        return False

    def check_permission_admin(self, user_id: int, chat_id: int):
        query = select(Chat).where(Chat.id == chat_id)
        chat = self.session.execute(query).scalars().first()
        if chat:
            if chat.creator.user_id == user_id:
                return True
        return False



@component
class UserRepo(BaseRepository, interfaces.UserRepo):

    def get(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        return user

    def check_user_login(self, user_login: str):
        query = select(User).where(User.login == user_login)
        if self.session.execute(query).scalars().one_or_none():
            return True
        return False

    def get_or_create(self, id_: Optional[int]) -> User:
        ...


@component
class ChatUserRepo(BaseRepository, interfaces.ChatUserRepo):

    def add(self, chatuser: ChatUser):
        self.session.add(chatuser)
        self.session.flush()

    # def get(self, chatuser_id: int):
    #     query = select(ChatUser).where(User.id == chatuser_id)
    #     return self.session.execute(query).scalars().one_or_none()

    def get_chatuser(self, user_id: int, chat_id: int) -> Optional[ChatUser]:
        query = select(ChatUser).where(and_(ChatUser.chat_id == chat_id, ChatUser.user_id == user_id))
        chatuser = self.session.execute(query).scalars().first()
        return chatuser

    def remove(self, chat_user: ChatUser):
        self.session.delete(chat_user)


@component
class MessageRepo(BaseRepository, interfaces.MessageRepo):

    def add(self, message: ChatMessage):
        self.session.add(message)
        self.session.flush()

    def get_by_id(self, message_id: int):
        query = select(ChatMessage).where(ChatMessage.id == message_id)
        message = self.session.execute(query).scalars().first()
        return message
