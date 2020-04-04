import jwt
import pendulum
from core.settings import settings


def create_password_hash(*, password: str):

    return settings.PASSWORD_CONTEXT.hash(password)


def verify_password(*, plain_password: str, hashed_password: str):

    return settings.PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_in_minutes: int):

    expire = pendulum.now().add(minutes=expires_in_minutes)

    data.update({"exp": expire})

    encoded_jwt = jwt.encode(
        payload=data, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt
