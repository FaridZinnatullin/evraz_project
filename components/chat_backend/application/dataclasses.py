from typing import List, Optional
import datetime
import attr


@attr.dataclass
class User:
    id: Optional[int] = None
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None


@attr.dataclass
class ChatUser:
    user: User
    chat: 'Chat'
    invite_date: datetime.datetime = datetime.datetime.now()
    leaved_date: datetime.datetime = None
    muted: bool = False
    banned: bool = False
    id: Optional[int] = None



# @attr.dataclass
# class ChatGroupUsers:
#     # chat: 'Chat'
#     members: List[ChatUser] = attr.ib(factory=list)
#     id: Optional[int] = None
#
#     def add_user(self, user: ChatUser):
#         if user not in self.members:
#             self.members.append(user)
#
#     def remove_user(self, user: ChatUser):
#         if user in self.members:
#             self.members.remove(user)


# @attr.dataclass
# class ChatBlackList(ChatGroupUsers):
#     pass
#
#
# @attr.dataclass
# class ChatSuperusers(ChatGroupUsers):
#     pass


@attr.dataclass
class ChatMessage:
    chat: 'Chat'
    user: User
    text: str
    send_date: datetime.datetime
    deleted: bool
    id: Optional[int] = None

    def delete_message(self):
        self.deleted = True


@attr.dataclass
class Chat:
    name: str
    #костыль, идей лучше нет
    tmp_id: int
    # blacklist: ChatBlackList
    # superusers: ChatSuperusers
    creator: Optional[User] = None
    messages: List[ChatMessage] = attr.ib(factory=list)
    members: List[ChatUser] = attr.ib(factory=list)
    id: Optional[int] = None


    def add_user(self, user: ChatUser):
        if user not in self.members:
            self.members.append(user)
        else:
            pass
            # выводим сообщение о том, что пользователь уже состоит в чате

    # def ban_user(self, user: ChatUser):
    #     if user not in self.blacklist.users:
    #         user.banned = True
    #         self.blacklist.users.append(user)
    #         self.members.remove(user)
    #     else:
    #         pass
    #         # выводим сообщение о том, что пользователь уже забанен
    #
    # def mute_user(self, user: ChatUser):
    #     if user not in self.blacklist.users:
    #         user.banned = True
    #         self.blacklist.users.append(user)
    #     else:
    #         pass
    #         # выводим сообщение о том, что пользователь уже замучен
