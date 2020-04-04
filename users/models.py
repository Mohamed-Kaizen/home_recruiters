import uuid
from enum import Enum

import pendulum
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Career(str, Enum):
    Electricians = "Electricians"
    Plumbers = "Plumbers"
    Mechanics = "Mechanics"


class User(models.Model):

    user_uuid = fields.UUIDField(unique=True, default=uuid.uuid4)

    username = fields.CharField(max_length=250, unique=True)

    email = fields.CharField(unique=True, max_length=400)

    password = fields.CharField(max_length=512)

    full_name = fields.TextField()

    phone_number = fields.CharField(max_length=10, unique=True)

    is_superuser = fields.BooleanField(default=False)

    is_staff = fields.BooleanField(
        default=False,
        description="Designates whether the user can log into this admin site.",
    )

    is_active = fields.BooleanField(
        default=True,
        description=""""Designates whether this user should be treated as active.
            Unselect this instead of deleting accounts.""",
    )

    career = fields.CharEnumField(enum_type=Career, max_length=200, null=True)

    is_worker = fields.BooleanField(
        default=False, description="Designates whether the user is worker.", null=True
    )

    is_customer = fields.BooleanField(
        default=False, description="Designates whether the user is customer.", null=True
    )

    date_joined = fields.DatetimeField(default=pendulum.now())

    def __str__(self) -> str:
        return f"{self.username}"

    class PydanticMeta:

        exclude = (
            "password",
            "id",
            "date_joined",
            "user_uuid",
            "is_superuser",
            "is_staff",
            "is_active",
        )


User_Pydantic = pydantic_model_creator(User, name="User")
