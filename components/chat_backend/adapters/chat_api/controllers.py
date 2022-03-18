import falcon
from classic.components import component
from classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)
from components.chat_backend.application import services
from .auth import Groups, Permissions
from .join_points import join_point



@component
class Chat:
    chat_manager: services.ChatManager

    #
    # @join_point
    # def on_get_chat_list(self, request, response):
    #     # тут вообще нужна проверка на то, просит ли юзер именно свои чаты или чужие
    #     chats = self.chat_manager.get_chats_by_userid(**request.params)
    #     response.media = {
    #         'chat_list': chats
    #     }
    #
    # @join_point
    # def on_get_chat_messages(self, request, response):
    #     messages = self.chat_manager.get_messages(request.params.get('chat_id'))
    #
    # @join_point
    # def on_get_chat_users(self, request, response):
    #     print('123')
    #     users = self.chat_manager.get_users(request.params.get('chat_id'))
    #     response.body = {
    #         '123': '456'
    #     }

    # создание юзера
    @join_point
    def on_post_create_user(self, request, response):
        self.chat_manager.create_user(**request.media)
        response.media = {
            'status': 'OK'
        }

    @join_point
    def on_get_get_user(self, request, response):
        user = self.chat_manager.get_user_by_id(**request.params)
        if user:
            result = {
                'user_id': user.id,
                'user_login': user.login,
                'user_password': user.password,
                'user_name': user.name
            }
            response.media = result
        else:
            response.status = falcon.HTTP_404

    @join_point
    def on_post_create_chat(self, request, response):
        self.chat_manager.create_chat(**request.media)
        response.media = {
            'status': 'OK'
        }

    @join_point
    def on_get_get_chat(self, request, response):
        chat = self.chat_manager.get_chat_by_id(**request.params)

        print('123')
        result = {
            'creator_id': chat.creator.user_id,
            'chat_members': chat.members,
            'chat_name': chat.name,
            'chat_creator_id': chat.creator.id
        }
        response.media = result



    # @join_point
    # def on_post_create_chat(self, request, response):
    #     user = request.get.
    #     self.chat_manager.create_chat(**request.media)


