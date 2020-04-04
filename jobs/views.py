from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from starlette import status
from tortoise.contrib.fastapi import HTTPNotFoundError

from . import interfaces, models, schema, services

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, description="Creating New Issue",
)
async def add_issue(
    user_input: schema.CreateIssue, auth_user: interfaces.current_customer = Depends()
) -> Dict[str, Any]:

    question = await services.IssueService().create_issue(
        issue=user_input, user=auth_user
    )

    customer = await question.customer

    return {"title": question.title, "customer": customer.username}


@router.get("/", description="Get ALL Issue")
async def list_of_open_issue() -> List[Dict[str, Any]]:

    issues = await services.IssueService().get_all_open_issue()

    issues_list = []

    for issue in issues:

        customer = await issue.customer

        issues_list.append(
            {
                "title": issue.title,
                "customer": customer.username,
                "city": issue.city,
                "sub_city": issue.sub_city,
                "is_open": issue.is_open,
                "is_negotiable": issue.is_negotiable,
                "issue_uuid": issue.issue_uuid,
            }
        )

    return issues_list


@router.get(
    "/{issue_uuid}/",
    response_model=models.Issue_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_issue(issue_uuid: str):
    return await services.IssueService().get_issue(issue_uuid=issue_uuid)
