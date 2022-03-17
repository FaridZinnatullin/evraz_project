from classic.app.errors import AppError


class NoPermission(AppError):
    msg_template = "You have no permissions to perform this action"
    # что это??
    code = 'chat.no_permissions'
