from core.settings import settings
from fastapi import Depends, HTTPException, status

from . import services, utils
from .models import User


async def current_user(token: str = Depends(settings.OAUTH2_SCHEME)) -> User:

    token_data = utils.verified_token(token)

    user = await services.UserServices().get_user_by_username(
        username=token_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def current_customer(token: str = Depends(settings.OAUTH2_SCHEME)) -> User:

    token_data = utils.verified_token(token)

    user = await services.UserServices().get_user_by_username(
        username=token_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not customer",
        )

    return user


async def current_worker(token: str = Depends(settings.OAUTH2_SCHEME)) -> User:

    token_data = utils.verified_token(token)

    user = await services.UserServices().get_user_by_username(
        username=token_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not Worker",
        )

    return user


# async def current_user_by_uuid(token: str = Depends(settings.OAUTH2_SCHEME)) -> User:
#
#     token_data = utils.verified_token(token)
#
#     user = await services.UserServices().get_user_by_user_id(user_id=token_data.user_id)
#
#     if user is None:
#         raise credentials_exception
#
#     return user
