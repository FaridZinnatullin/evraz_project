from datetime import datetime
from unittest.mock import Mock
import attr
import pytest

from components.chat_backend.application import interfaces, dataclasses


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        name='testing_name',
        login='testing_login',
        password='testing_password',
        id=1,
    )

@attr.dataclass
class creator:
    user_id = 1


@pytest.fixture(scope='function')
def chat():
    return dataclasses.Chat(
        creator=creator,
        messages=[1, 2],
        members=[1, 2, 3],
        name='testing_chat_name',
        id=1
    )


@pytest.fixture(scope='function')
def chat_user():
    return dataclasses.ChatUser(
        user=1,
        chat=1,
        invite_date=datetime.now(),
        leaved_date=None,
        muted=False,
        banned=False,
        id=1
    )


@pytest.fixture(scope='function')
def chat_messages():
    return dataclasses.ChatMessage(
        chatuser=1,
        text='testing text for message',
        send_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        deleted=False,
        id=1,
    )


@pytest.fixture(scope='function')
def user_repo(user):
    user_repo = Mock(interfaces.UserRepo)
    user_repo.get = Mock(return_value=user)
    return user_repo


@pytest.fixture(scope='function')
def chats_repo(chat):
    chats_repo = Mock(interfaces.ChatRepo)
    chats_repo.get = Mock(return_value=chat)
    return chats_repo


@pytest.fixture(scope='function')
def chat_messages_repo(chat_messages):
    chat_messages_repo = Mock(interfaces.MessageRepo)
    chat_messages_repo.get_by_id = Mock(return_value=chat_messages)
    return chat_messages_repo


@pytest.fixture(scope='function')
def chats_user_repo(chat_user):
    chats_user_repo = Mock(interfaces.ChatUserRepo)
    chats_user_repo.get_chatuser = Mock(return_value=chat_user)
    return chats_user_repo