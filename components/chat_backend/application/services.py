from typing import List, Optional

from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments
from classic.app import DTO, validate_with_dto

import jwt
from . import errors, interfaces
from .dataclasses import User, ChatUser, Chat, ChatMessage

# разобрать что это и зачем
join_points = PointCut()
join_point = join_points.join_point


# class ChatInfo(DTO):
#     name: str
#     members: List[ChatUser] = None

class UserInfo(DTO):
    name: str
    login: str
    password: str



@component
class ChatManager:
    chats_repo: interfaces.ChatRepo
    user_repo: interfaces.UserRepo
    chats_user_repo: interfaces.ChatUserRepo
    messages_repo: interfaces.MessageRepo

    @join_point
    def create_chat(self, chat_name: str, user_id: int, member_ids: Optional[List[int]] = None):
        chat = Chat(name=chat_name)
        chat = self.chats_repo.add(chat)
        chat_user = self.create_chatuser(user_id=user_id, chat_id=chat.id)
        chat.creator = chat_user

        # TODO: отправлять JSON через postman
        for member in member_ids:
            member_chatuser = self.create_chatuser(user_id=member, chat_id=chat.id)
            chat.add_user(member_chatuser)

        self.chats_repo.add(chat)


    @join_point
    @validate_arguments
    def delete_chat(self, user_id: int, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        if chat.creator.user_id != user_id:
            raise errors.NoPermission()
        else:
            self.chats_repo.remove(chat)

    @join_point
    @validate_arguments
    def rename_chat(self, user_id: int, chat_id: int, new_name: str):
        chat = self.get_chat_by_id(chat_id)
        if chat.creator.user_id != user_id:
            raise errors.NoPermission()
        else:
            chat.name = new_name
            self.chats_repo.add(chat)


    @join_point
    @validate_arguments
    def create_user(self, name: str, login: str, password: str):
        user = User(name=name, login=login, password=password)
        user = self.user_repo.add(user)
        return user


    @join_point
    @validate_arguments
    def create_chatuser(self, user_id: int, chat_id: int):
        user = self.get_user_by_id(user_id)
        chat = self.get_chat_by_id(chat_id)
        chat_user = ChatUser(user=user, chat=chat)
        self.chats_user_repo.add(chat_user)

        return chat_user

    @join_point
    @validate_arguments
    def get_all_chatusers(self, user_id: int, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        chat_user = self.get_chat_user(user_id, chat_id)
        if chat_user in chat.members:
            return chat.members
        else:
            raise errors.NoPermission()

    @join_point
    @validate_arguments
    def create_message(self, user_id: int, chat_id: int, message: str):
        user = self.get_user_by_id(user_id)
        chat = self.get_chat_by_id(chat_id)
        #прверка доступа
        if self.chats_repo.check_permission_member(user_id=user_id, chat_id=chat_id):
            chat_user = self.chats_user_repo.get_chatuser(user_id, chat_id)
            message = ChatMessage(chatuser=chat_user, text=message)
            chat.add_message(message)
            self.messages_repo.add(message)
            self.chats_repo.add(chat)
        else:
            raise errors.NoPermission()

    @join_point
    @validate_arguments
    def get_all_chat_messages(self, user_id: int, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        if self.chats_repo.check_permission_member(user_id=user_id, chat_id=chat_id):
            return chat.messages


    # @join_point
    # @validate_arguments
    # def get_chat_messages(self, chat_id: int):
    #     messages = self.chats_repo.get_all_messages(chat_id)
    #     return messages
    #
    @join_point
    @validate_arguments
    def get_chat_user(self, user_id: int, chat_id: int):
        users = self.chats_user_repo.get_chatuser(user_id, chat_id)
        return users

    @join_point
    @validate_arguments
    def get_chat_by_id(self, chat_id: int):
        chat = self.chats_repo.get(chat_id)
        return chat

    @join_point
    def get_user_by_id(self, user_id: int):
        user = self.user_repo.get(user_id)
        if not user:
            raise errors.UncorrectedParams()
        return user

    @join_point
    @validate_with_dto
    def registration(self, user_data: UserInfo):
        if self.user_repo.check_user_login(user_data.login):
            raise errors.UserAlreadyExist()
        else:
            user = user_data.create_obj(User)
            user = self.user_repo.add(user)
            # TODO: выкинуть этот процесс в auth.py, а токен в env
            token = jwt.encode(
                {
                    "sub": user.id,
                    "login": user.login,
                    "name": user.name,
                    "group": "User"
                },
                'this_is_secret_key_for_jwt',
                algorithm="HS256"
            )
            return token






