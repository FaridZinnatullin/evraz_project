from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import User, ChatUser, Chat, ChatMessage, ChatBlackList, ChatSuperusers


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]:
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
    def add(self, customer: User):
        ...


class ChatRepo(ABC):

    @abstractmethod
    def add(self, chat: Chat):
        ...

    @abstractmethod
    def remove(self, chat: Chat):
        ...

    # вопрос о том, какая именно инфо
    @abstractmethod
    def get_info(self, chat: Chat):
        ...

    @abstractmethod
    def get_all_users(self, chat: Chat) -> List[User]:
        ...

    @abstractmethod
    def get_all_messages(self, chat: Chat) -> List[ChatMessage]:
        ...


class MessageRepo(ABC):

    @abstractmethod
    def add(self, message: ChatMessage):
        ...


class ChatBlackListRepo(ABC):

    @abstractmethod
    def add(self, blacklist: ChatBlackList):
        ...

    @abstractmethod
    def get_users(self, blacklist: ChatBlackList) -> List[User]:
        ...

    @abstractmethod
    def clean(self, blacklist: ChatBlackList):
        ...


class ChatSuperusersRepo(ABC):

    @abstractmethod
    def add(self, superusers: ChatSuperusers):
        ...

    @abstractmethod
    def get_users(self, superusers: ChatSuperusers) -> List[User]:
        ...

    @abstractmethod
    def clean(self, superusers: ChatSuperusers):
        ...
