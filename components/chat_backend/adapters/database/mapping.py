from sqlalchemy.orm import registry, relationship

from ...application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)

mapper.map_imperatively(dataclasses.ChatUser, tables.chat_users)

mapper.map_imperatively(dataclasses.ChatMessage, tables.chat_messages)

mapper.map_imperatively(
    dataclasses.Chat,
    tables.chats,
    properties={
        'members': relationship(dataclasses.ChatUser, lazy='subquery'),
        'messages': relationship(dataclasses.ChatMessage, lazy='subquery')
    }
)

mapper.map_imperatively(
    dataclasses.ChatBlackList,
    tables.chat_blacklist,
    properties={
        'users': relationship(dataclasses.ChatUser, lazy='subquery')
    }
)

mapper.map_imperatively(
    dataclasses.ChatSuperusers,
    tables.chat_superusers,
    properties={
        'users': relationship(dataclasses.ChatUser, lazy='subquery')
    }
)
