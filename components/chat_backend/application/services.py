import os
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


class RenameChatInfo(DTO):
    user_id: int
    chat_id: int
    new_name: int


class CreateMessageInfo(DTO):
    user_id: int
    chat_id: int
    message: str


class UserInfo(DTO):
    name: str
    login: str
    password: str

class UserLoginInfo(DTO):
    login: str
    password: str


class BanUserInfo(DTO):
    user_id: int
    banned_user_id: int
    chat_id: int


class AddToChatInfo(DTO):
    user_id: int
    invited_user_id: int
    chat_id: int


class CreateChatInfo(DTO):
    chat_name: str
    user_id: int
    member_ids: Optional[List[int]]


@component
class ChatManager:
    chats_repo: interfaces.ChatRepo
    user_repo: interfaces.UserRepo
    chats_user_repo: interfaces.ChatUserRepo
    chat_messages_repo: interfaces.MessageRepo

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: CreateChatInfo):
        chat = Chat(name=chat_info.chat_name)
        chat = self.chats_repo.add(chat)
        chat_user = self.create_chatuser(user_id=chat_info.user_id, chat_id=chat.id)
        chat.creator = chat_user

        for member_id in chat_info.member_ids:
            if member_id != chat_info.user_id:
                member_chatuser = self.create_chatuser(user_id=member_id, chat_id=chat.id)
                chat.add_user(member_chatuser)

        self.chats_repo.add(chat)

    @join_point
    @validate_arguments
    def delete_chat(self, user_id: int, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        if chat:
            if chat.creator.user_id != user_id:
                raise errors.NoPermission()
            else:
                self.chats_repo.remove(chat)
        else:
            raise errors.UncorrectedParams()

    @join_point
    @validate_arguments
    def comeback_to_chat(self, user_id: int, chat_id: int):
        chatuser = self.get_chat_user(user_id, chat_id)
        chat = self.get_chat_by_id(chat_id=chat_id)
        if chatuser:
            if chatuser.banned:
                raise errors.BannedUser()
            raise errors.UncorrectedParams()
        if chat:
            self.create_chatuser(user_id, chat_id)
        else:
            raise errors.UncorrectedParams()

    @join_point
    @validate_arguments
    def add_to_chat(self, add_to_chat_info: AddToChatInfo):
        chat_user = self.get_chat_user(AddToChatInfo.invited_user_id, AddToChatInfo.chat_id)
        if self.chats_repo.check_permission_admin(add_to_chat_info.user_id, add_to_chat_info.chat_id) and not chat_user:
            self.create_chatuser(AddToChatInfo.invited_user_id, AddToChatInfo.chat_id)

    @join_point
    @validate_arguments
    def leave_chat(self, user_id: int, chat_id: int):
        chatuser = self.get_chat_user(user_id, chat_id)
        # проверка, является ли пользователь участником чата...
        if self.chats_repo.check_permission_member(user_id, chat_id):
            # проверка, является ли пользователь создателем чата...
            if self.chats_repo.check_permission_admin(user_id, chat_id):
                # удаляем чат вмесие со всеми чатюзерами
                self.delete_chat(user_id, chat_id)
            else:
                self.chats_user_repo.remove(chatuser)

    @join_point
    @validate_with_dto
    def ban_user(self, ban_info: BanUserInfo):
        chatuser = self.get_chat_user(ban_info.banned_user_id, ban_info.chat_id)
        if self.chats_repo.check_permission_member(ban_info.banned_user_id,
                                                   ban_info.chat_id) and self.chats_repo.check_permission_admin(
            ban_info.user_id, ban_info.chat_id):
            chatuser.banned = True
            self.chats_user_repo.add(chatuser)
        else:
            raise errors.UncorrectedParams()

    @join_point
    @validate_with_dto
    def rename_chat(self, rename_info: RenameChatInfo):
        chat = self.get_chat_by_id(rename_info.chat_id)
        if chat.creator.user_id != rename_info.user_id:
            raise errors.NoPermission()
        else:
            chat.name = rename_info.new_name
            self.chats_repo.add(chat)

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
        if self.chats_repo.check_permission_member(user_id=user_id, chat_id=chat_id):
            return chat.members
        else:
            raise errors.NoPermission()

    # TODO: Воткнуть ДТО
    @join_point
    @validate_arguments
    def create_message(self, message_info: CreateMessageInfo):
        chat = self.get_chat_by_id(message_info.chat_id)
        # прверка доступа
        if self.chats_repo.check_permission_member(user_id=message_info.user_id, chat_id=message_info.chat_id):
            chat_user = self.chats_user_repo.get_chatuser(message_info.user_id, message_info.chat_id)
            message = ChatMessage(chatuser=chat_user, text=message_info.message)
            chat.add_message(message)
            self.chat_messages_repo.add(message)
            self.chats_repo.add(chat)
        else:
            raise errors.NoPermission()

    @join_point
    @validate_arguments
    def get_all_chat_messages(self, user_id: int, chat_id: int):
        chat = self.get_chat_by_id(chat_id)
        if not chat:
            raise errors.UncorrectedParams()
        if self.chats_repo.check_permission_member(user_id=user_id, chat_id=chat_id):
            return chat.messages

    @join_point
    @validate_arguments
    def get_message_by_id(self, message_id: int):
        message = self.chat_messages_repo.get_by_id(message_id)
        if not message:
            raise errors.UncorrectedParams()
        return message

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
    @validate_arguments
    def get_chat_by_id_public(self, chat_id: int, user_id: int):
        if self.chats_repo.check_permission_member(chat_id=chat_id, user_id=user_id):
            chat = self.chats_repo.get(chat_id)
            return chat
        else:
            raise errors.NoPermission()

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

            return user

    @join_point
    @validate_with_dto
    def login(self, user_data: UserLoginInfo):
        user = self.user_repo.authorization(user_data.login, user_data.password)
        if user:
            return user
        else:
            raise errors.UncorrectedLoginPassword()
