from typing import List

from fastapi import HTTPException, status
from tortoise import exceptions as tortoise_exceptions

from .models import Issue, Issue_Pydantic
from .schema import CreateIssue


class IssueService:
    @staticmethod
    async def get_all_open_issue() -> List[Issue]:
        return await Issue.filter(is_open=True)

    @staticmethod
    async def get_issue(*, issue_uuid: str):
        return await Issue_Pydantic.from_queryset_single(
            Issue.get(issue_uuid=issue_uuid)
        )

    @staticmethod
    async def create_issue(*, issue: CreateIssue, user) -> Issue:
        try:
            issue = await Issue.create(
                title=issue.title,
                description=issue.description,
                city=issue.city,
                sub_city=issue.sub_city,
                time_to_come_from=issue.time_to_come_from,
                time_to_come_to=issue.time_to_come_to,
                amount_from=issue.amount_from,
                amount_to=issue.amount_to,
                is_negotiable=issue.is_negotiable,
                is_open=issue.is_open,
                customer=user,
            )

            return issue

        except tortoise_exceptions.IntegrityError:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question with {issue.title} already exists.",
            )
