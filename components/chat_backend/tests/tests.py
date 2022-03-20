from datetime import datetime

import pydantic
import pytest
import attr
from conftest import creator
from components.chat_backend.application import errors
from attr import asdict

from components.chat_backend.application.services import ChatManager


# @pytest.fixture(scope='function')
# def service_user(user_repo):
#     return Users(user_repo=user_repo)


@pytest.fixture(scope='function')
def service_chat(user_repo, chats_repo, chats_user_repo, chat_messages_repo):
    return ChatManager(user_repo=user_repo, chats_repo=chats_repo, chats_user_repo=chats_user_repo,
                       chat_messages_repo=chat_messages_repo)


data_user = {
    'login': 'testing_login',
    'password': 'testing_password',
    'name': 'testing_name',
    'id': 1,
}

data_message = {
    'id': 1,
    'chatuser': 1,
    'text': 'testing text for message',
    'deleted': False,
    'send_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

data_add_message = {
    'user_id': 2,
    'chat_id': 1,
    'message': 'test message'
}

data_rename_chat = {
    'user_id': 1,
    'chat_id': 1,
    'new_name': 'new name',
}

data_chat = {
    'creator': 1,
    'messages': [1, 2],
    'members': [1, 2, 3],
    'name': 'testing_chat_name',
    'id': 1
}

data_chat_user = {
    'user_id': 1,
    'chat_id': 1,
}

data_create_chat = {
    'chat_name': 'test chat name',
    'user_id': 1,
    'member_ids': None
}


data_chat_with_creator = {
    'creator': creator,
    'messages': [1, 2],
    'members': [1, 2, 3],
    'name': 'testing_chat_name',
    'id': 1
}

data_chat_msg = {
    'chat_id': 1,
    'user_id': 1,
    'text': 'my msg',
    'id': 1,
    'send_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
}


def test_registration(service_chat):
    with pytest.raises(errors.UserAlreadyExist):
        service_chat.registration(**data_user)
        service_chat.user_repo.add.assert_called_once()


def test_get_user(service_chat):
    user = service_chat.get_user_by_id(user_id=1)
    assert asdict(user) == data_user


def test_add_chat(service_chat):
    with pytest.raises(pydantic.ValidationError):
        service_chat.create_chat(chat_name='str', user_id=1, member_ids=None)


def test_rename_chat(service_chat):
    service_chat.rename_chat(**data_rename_chat)
    service_chat.chats_repo.add.assert_called_once()


def test_get_chat(service_chat):
    chat = service_chat.get_chat_by_id(chat_id=1)
    assert asdict(chat) == data_chat_with_creator


def test_add_chat_user(service_chat):
    service_chat.create_chatuser(**data_chat_user)
    service_chat.chats_user_repo.add.assert_called_once()


def test_add_chat_message(service_chat):
    service_chat.create_message(**data_add_message)
    service_chat.chat_messages_repo.add.assert_called_once()


def test_get_chat_user(service_chat):
    members = service_chat.get_chat_user(user_id=1, chat_id=1)
    members_dict = asdict(members)
    assert members_dict.get('chat') == data_chat_user.get('chat_id') and \
           members_dict.get('user') == data_chat_user.get('user_id')


def test_get_chat_message(service_chat):
    messages = service_chat.get_message_by_id(message_id=1)
    assert asdict(messages) == data_message
