from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User, ChatUser, Chat, ChatMessage


class UserRepo(ABC):

    @abstractmethod
    def get(self, id_: int) -> Optional[User]:
        print('Абстракция?')
        ...

    @abstractmethod
    def add(self, customer: User):
        ...

    #зачем?
    @abstractmethod
    def get_or_create(self, id_: Optional[int]) -> User:
        ...


class ChatUserRepo(ABC):

    @abstractmethod
    def add(self, customer: ChatUser):
        ...


class ChatRepo(ABC):

    @abstractmethod
    def add(self, chat: Chat):
        ...

    @abstractmethod
    def remove(self, chat: Chat):
        ...

    @abstractmethod
    def get(self, chat_id: int):
        ...

    # вопрос о том, какая именно инфо
    @abstractmethod
    def get_info(self, chat: Chat):
        ...

    @abstractmethod
    def get_all_users(self, id_chat: int) -> List[ChatUser]:
        ...

    @abstractmethod
    def get_all_messages(self, id_chat: int) -> List[ChatMessage]:
        ...

    @abstractmethod
    def get_chat_by_tmp_id(self, tmp_id: int) -> Chat:
        ...

    # @abstractmethod
    # def get_all_chats_by_user(self, id_user: int) -> List[Chat]:
    #     ...

    # @abstractmethod
    # def get_all_chats_by_user_id(self, id_user: int) -> List[Chat]:
    #     pass


class MessageRepo(ABC):

    @abstractmethod
    def add(self, message: ChatMessage):
        ...


# class ChatBlackListRepo(ABC):
#
#     @abstractmethod
#     def add(self, blacklist: ChatBlackList):
#         ...
#
#     @abstractmethod
#     def get_users(self, blacklist: ChatBlackList) -> List[User]:
#         ...
#
#     @abstractmethod
#     def clean(self, blacklist: ChatBlackList):
#         ...
#
#
# class ChatSuperusersRepo(ABC):
#
#     @abstractmethod
#     def add(self, superusers: ChatSuperusers):
#         ...
#
#     @abstractmethod
#     def get_users(self, superusers: ChatSuperusers) -> List[User]:
#         ...
#
#     @abstractmethod
#     def clean(self, superusers: ChatSuperusers):
#         ...
