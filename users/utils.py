import jwt
import pendulum
from core.settings import settings
from fastapi import HTTPException, status
from jwt import PyJWTError

from . import schema


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


def verified_token(token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM,
            verify=True,
        )

        token_data = schema.TokenData(
            username=payload.get("sub"),
            exp=payload.get("exp"),
            user_uuid=payload.get("user_uuid"),
        )

    except PyJWTError:
        raise credentials_exception

    return token_data
