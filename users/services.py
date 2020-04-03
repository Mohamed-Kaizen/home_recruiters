from typing import Dict

from .models import User
from .utils import create_password_hash


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
        )

        return user
