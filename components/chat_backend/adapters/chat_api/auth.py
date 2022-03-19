from classic.http_auth import Group, Permission, strategies
import os
from dotenv import load_dotenv

class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL, ))


# dummy_strategy = strategies.Dummy(
#     user_id=1,
#     login='dummy',
#     name='Admin dummy',
#     groups=(Groups.ADMINS.name, ),
# )


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


SECRET_JWT_KEY = os.getenv('SECRET_JWT_KEY')



jwt_strategy = strategies.JWT(
    secret_key='this_is_secret_key_for_jwt',
    # algorithms=['MD-5']
)

ALL_GROUPS = (Groups.ADMINS, )
