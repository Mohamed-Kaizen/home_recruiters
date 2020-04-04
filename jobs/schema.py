from datetime import datetime

from pydantic import BaseModel, Field

from .models import City, SubCity


class CreateIssue(BaseModel):

    title: str = Field(..., max_length=255)

    description: str

    city: City

    sub_city: SubCity

    description: str

    time_to_come_from: datetime

    time_to_come_to: datetime

    amount_from: int = 0

    amount_to: int = 0

    is_negotiable: bool

    is_open: bool


class UpdateIssue(BaseModel):

    is_open: bool
