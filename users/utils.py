from core.settings import settings


def create_password_hash(*, password: str):

    return settings.PASSWORD_CONTEXT.hash(password)
