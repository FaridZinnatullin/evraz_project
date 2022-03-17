from typing import List, Optional, Tuple
import random
from pydantic import conint, validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import User, ChatUser, Chat, ChatMessage

# разобрать что это и зачем
join_points = PointCut()
join_point = join_points.join_point


# class ChatInfo(DTO):
#     name: str
#     members: List[ChatUser] = None


@component
class ChatManager:
    chats_repo: interfaces.ChatRepo
    user_repo: interfaces.UserRepo
    chats_user_repo: interfaces.ChatUserRepo
    # chat_blacklist_repo: interfaces.ChatBlackListRepo
    # chat_superusers_repo: interfaces.ChatSuperusersRepo

    @join_point
    def create_chat(self, chat_name:str, user_id: int):
        print('124')
        tmp_id = random.randint(1, 10000)
        chat = Chat(name=chat_name, tmp_id=tmp_id)
        self.chats_repo.add(chat)

        chat = self.get_chat_by_tmp_id(tmp_id)
        chat_user = self.create_chatuser(user_id=user_id, chat_id=chat.id)
        chat.creator = chat_user

        if members:
            for member in members:
                chat_user = self.create_chatuser(user_id=member.id, chat_id=chat.id)
                chat.add_user(chat_user)

        self.chats_repo.add(chat)

    @join_point
    # @validate_arguments
    def create_user(self, name: str, login: str, password: str):
        user = User(name=name, login=login, password=password)
        user = self.user_repo.add(user)
        return user

    @join_point
    def get_chat_by_tmp_id(self, tmp_id: int):
        chat = self.chats_repo.get_chat_by_tmp_id(tmp_id)
        return chat


    @join_point
    @validate_arguments
    def create_chatuser(self, user_id: int, chat_id: int):
        user = self.get_user_by_id(user_id)
        chat = self.get_chat_by_id(chat_id)
        chat_user = ChatUser(user=user, chat=chat)
        self.chats_user_repo.add(chat_user)

        return chat_user

    # @join_point
    # @validate_arguments
    # def create_blacklist_by_chat_id(self, chat_id):
    #     # chat = self.get_chat_by_id(chat_id)
    #     blacklist = ChatBlackList()
    #     blacklist = self.chat_blacklist_repo.add(blacklist)
    #     return blacklist
    #
    # @join_point
    # @validate_arguments
    # def create_superusers_by_chat_id(self, chat_id):
    #     # chat = self.get_chat_by_id(chat_id)
    #     superusers = ChatSuperusers()
    #     superusers = self.chat_superusers_repo.add(superusers)
    #     return superusers

    # @join_point
    # @validate_arguments
    # def get_chats(self, user_id: int):
    #     chats = self.chats_repo.get_all_chats_by_user_id(user_id)
    #     return chats

    @join_point
    @validate_arguments
    def get_chat_messages(self, chat_id: int):
        messages = self.chats_repo.get_all_messages(chat_id)
        return messages

    @join_point
    @validate_arguments
    def get_chat_users(self, chat_id: int):
        users = self.chats_repo.get_all_users(chat_id)
        return users

    @join_point
    @validate_arguments
    def get_chat_by_id(self, chat_id: int):
        chat = self.chats_repo.get(chat_id)
        return chat

    @join_point
    def get_user_by_id(self, user_id: int):
        user = self.user_repo.get(user_id)
        result = {
            'user_login': user.login,
            'user_password': user.password,
            'user_name': user.name
        }
        return result
