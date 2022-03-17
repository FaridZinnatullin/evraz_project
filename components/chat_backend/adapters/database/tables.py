from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Boolean,
    DateTime,
    BigInteger,
    Text
)
import datetime

# разобрать что за naming convention
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

users = Table(
    'Users',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    Column('login', String(50), nullable=False),
    Column('password', String(13), nullable=False),
)

chat_users = Table(
    'ChatUsers',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('User.id')),
    Column('chat_id', Integer, ForeignKey('Chat.id')),
    Column('muted', Boolean, default=False),
    Column('banned', Boolean, default=False),
    Column('invite_date', DateTime, default=datetime.datetime.utcnow()),
    Column('leaved_date', DateTime, nullable=True),

)

chats = Table(
    'Chats',
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    # relationship('messages', 'ChatMessage'),
    # relationship('members', 'ChatUser'),
    Column('blacklist_id', Integer, ForeignKey('Blacklist.id')),
    Column('superusers_id', Integer, ForeignKey('Superusers.id')),
)

chat_messages = Table(
    'ChatMessages',
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('chat_id', Integer, ForeignKey('Chat.id')),
    Column('user_id', Integer, ForeignKey('ChatUser.id')),
    Column('text', Text, nullable=False),
    Column('send_date', DateTime, default=datetime.datetime.utcnow()),
    Column('deleted', Boolean, default=False),
)

chat_blacklist = Table(
    'ChatBlackList',
    Column('id', Integer, primary_key=True, autoincrement=True),
    # Column('chat', Integer, ForeignKey('Chat.id'), nullable=True),
)

chat_superusers = Table(
    'ChatSuperusers',
    Column('id', Integer, primary_key=True, autoincrement=True),
    # Column('chat', Integer, ForeignKey('Chat.id'), nullable=True),
)
