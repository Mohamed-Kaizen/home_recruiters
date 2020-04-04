from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError

from . import interfaces, models, schema, services
from .models import Issue

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


@router.post("/{issue_uuid}/", status_code=status.HTTP_200_OK)
async def update_issue_state(
    issue_uuid: str,
    user_input: schema.UpdateIssue,
    auth_user: interfaces.current_customer = Depends(),
):
    has_updated = await Issue.filter(issue_uuid=issue_uuid, customer=auth_user).update(
        **user_input.dict(exclude_unset=True)
    )

    if not has_updated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the owner",
        )

    return {"detail": "The issue has been updated"}


@router.get(
    "/{issue_uuid}/",
    response_model=models.Issue_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_issue(issue_uuid: str):
    return await services.IssueService().get_issue(issue_uuid=issue_uuid)
