from typing import List, Optional, Tuple

from pydantic import conint, validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import User, ChatUser, Chat, ChatMessage, ChatSuperusers, ChatBlackList

# разобрать что это и зачем
join_points = PointCut()
join_point = join_points.join_point


@component
class ChatManager:
    chats_repo: interfaces.ChatRepo
    user_repo: interfaces.UserRepo
    chat_blacklist_repo: interfaces.ChatBlackListRepo
    chat_superusers_repo: interfaces.ChatSuperusersRepo

    @join_point
    @validate_arguments
    def create_chat(self, name: str, creator: User, members: Optional[List[User]]): # Optional[List[User]] - может ли такое вообще жить?
        blacklist = ChatBlackList()
        superusers = ChatSuperusers()

        chat = Chat(name=name,
                    blacklist=blacklist,
                    superusers=superusers,
                    )
        chat_creator = ChatUser(user=creator, chat=chat)
        chat.superusers.add_user(chat_creator)
        if members:
            for member in members:
                chat_user = ChatUser(user=member, chat=chat)
                chat.add_user(chat_user)

        self.chat_superusers_repo.add(superusers)
        self.chat_blacklist_repo.add(blacklist)
        self.chats_repo.add(chat)

    def get_chats(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        chats = self.chats_repo.get_chats_by_user(user)
        return chats

    def get_chat_messages(self, chat_id: int):
        messages = self.chats_repo.get_all_messages(chat_id)
        return messages

    def get_chat_users(self, chat_id: int):
        users = self.chats_repo.get_all_users(chat_id)
        return users


