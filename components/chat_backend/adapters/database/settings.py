from pydantic import BaseSettings


# РАЗОБРАТЬ ALEMBIC
class Settings(BaseSettings):
    DB_URL: str = ''