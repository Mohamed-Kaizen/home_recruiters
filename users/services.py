from typing import Dict, List, Optional

from fastapi import HTTPException, status
from tortoise import exceptions as tortoise_exceptions

from .models import User
from .schema import CustomerCreate, WorkerCreate
from .utils import create_password_hash, verify_password


class UserServices:
    @staticmethod
    async def create_super_user(data: Dict) -> User:

        password = create_password_hash(password=data.get("password"))

        user = await User.create(
            username=data.get("username"),
            email=data.get("email"),
            full_name=data.get("full_name"),
            password=password,
            is_superuser=data.get("is_superuser"),
            is_staff=data.get("is_staff"),
            is_active=data.get("is_active"),
            phone_number=data.get("phone_number"),
        )

        return user

    async def authenticate(self, *, username: str, password: str) -> Optional[User]:
        user = await self.get_user_by_username(username=username)

        if not user:
            return None

        if not verify_password(plain_password=password, hashed_password=user.password):

            return None

        return user

    @staticmethod
    async def get_user_by_username(*, username: str) -> Optional[User]:

        try:

            user = await User.get(username=username)

            return user

        except tortoise_exceptions.DoesNotExist:

            return None

    @staticmethod
    async def get_all_users() -> List[User]:

        return await User.all()

    @staticmethod
    async def get_all_customers() -> List[User]:

        return await User.filter(is_customer=True)

    @staticmethod
    async def get_all_workers() -> List[User]:

        return await User.filter(is_worker=True)

    @staticmethod
    async def create_worker(*, user: WorkerCreate) -> User:

        password = create_password_hash(password=user.password)

        try:
            user = await User.create(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                password=password,
                phone_number=user.phone_number,
                career=user.career,
                is_worker=True,
            )

            return user

        except tortoise_exceptions.IntegrityError:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username or email or phone number already exists.",
            )

    @staticmethod
    async def create_customer(*, user: CustomerCreate) -> User:

        password = create_password_hash(password=user.password)

        try:
            user = await User.create(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                password=password,
                phone_number=user.phone_number,
                is_customer=True,
            )

            return user

        except tortoise_exceptions.IntegrityError:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username or email or phone number already exists.",
            )
