import uuid
from enum import Enum

from core.utils import get_user_model
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

User = get_user_model()


class City(str, Enum):
    addis_ababa = "Addis Ababa"


class SubCity(str, Enum):
    lafto = "Lafto"
    saris = "Saris"
    stadium = "Stadium"
    merkato = "Merkato"
    jemo = "Jemo"


class Issue(models.Model):

    issue_uuid = fields.UUIDField(unique=True, default=uuid.uuid4)

    title = fields.CharField(max_length=255)

    description = fields.TextField()

    customer = fields.ForeignKeyField(
        "models.User", related_name="issues", on_delete=fields.CASCADE
    )

    city = fields.CharEnumField(enum_type=City, max_length=400)

    sub_city = fields.CharEnumField(enum_type=SubCity, max_length=200)

    time_to_come_from = fields.DatetimeField()

    time_to_come_to = fields.DatetimeField()

    amount_from = fields.IntField(null=True)

    amount_to = fields.IntField(null=True)

    is_negotiable = fields.BooleanField(default=False)

    is_open = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"


Issue_Pydantic = pydantic_model_creator(Issue, name="Issue")
