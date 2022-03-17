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
class ChatList:
    chats_repo: interfaces.ChatRepo
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
