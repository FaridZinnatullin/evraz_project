from classic.app.errors import AppError


class NoPermission(AppError):
    msg_template = "You have no permissions to perform this action"
    code = 'chat.no_permissions'


class UserAlreadyExist(AppError):
    msg_template = "This login is already occupied"
    code = 'chat.user_already_exist'


class UncorrectedParams(AppError):
    msg_template = "You give me very bad params... I have no data for you"
    code = 'chat.bad_params'


class BannedUser(AppError):
    msg_template = "This user was banned in this chat"
    code = 'chat.banned_user'


class UncorrectedLoginPassword(AppError):
    msg_template = "Incorrect username or password"
    code = 'chat.authorization'
