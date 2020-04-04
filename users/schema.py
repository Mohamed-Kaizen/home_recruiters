from typing import List

from core.settings import settings
from pydantic import BaseModel, EmailStr, Field, validator

from . import validators
from .models import Career


class WorkerCreate(BaseModel):

    username: str = Field(..., min_length=1, max_length=250)

    password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )

    email: EmailStr

    full_name: str = Field(..., max_length=400)

    phone_number: str = Field(..., min_length=9, max_length=10)

    career: Career

    @validator("username")
    def extra_validation_on_username(cls, value: str):
        validators.validate_reserved_name(value=value, exception_class=ValueError)

        validators.validate_confusables(value=value, exception_class=ValueError)

        return value

    @validator("email")
    def extra_validation_on_email(cls, value: str):

        local_part, domain = value.split("@")

        validators.validate_reserved_name(value=local_part, exception_class=ValueError)

        validators.validate_confusables_email(
            domain=domain, local_part=local_part, exception_class=ValueError
        )

        return value


class UserList(BaseModel):

    username: List[str]


class WorkerList(BaseModel):

    username: List[str]

    career: Career


class CustomerCreate(BaseModel):

    username: str = Field(..., min_length=1, max_length=250)

    password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )

    email: EmailStr

    full_name: str = Field(..., max_length=400)

    phone_number: str = Field(..., min_length=9, max_length=10)

    @validator("username")
    def extra_validation_on_username(cls, value: str):
        validators.validate_reserved_name(value=value, exception_class=ValueError)

        validators.validate_confusables(value=value, exception_class=ValueError)

        return value

    @validator("email")
    def extra_validation_on_email(cls, value: str):

        local_part, domain = value.split("@")

        validators.validate_reserved_name(value=local_part, exception_class=ValueError)

        validators.validate_confusables_email(
            domain=domain, local_part=local_part, exception_class=ValueError
        )

        return value
