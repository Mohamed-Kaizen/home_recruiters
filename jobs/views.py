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

    issue = await services.IssueService().create_issue(issue=user_input, user=auth_user)

    customer = await issue.customer

    return {"title": issue.title, "customer": customer.username}


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


@router.post(
    "/offer/", status_code=status.HTTP_201_CREATED, description="Creating New Offer",
)
async def add_offer(
    user_input: schema.CreateOffer, auth_user: interfaces.current_customer = Depends()
) -> Dict[str, Any]:

    offer = await services.OfferService().create_offer(offer=user_input, user=auth_user)

    return {"customer": offer.from_customer, "worker": offer.to_worker}


@router.get("/offer/")
async def get_all_offer(auth_user: interfaces.current_worker = Depends()):

    offers = await services.OfferService().get_offers(user=auth_user)

    offers_list = []

    for offer in offers:

        offers_list.append(
            {
                "offer_uuid": offer.offer_uuid,
                "user": offer.to_worker,
                "customer": offer.from_customer,
                "worker_has_read_it": offer.worker_has_read_it,
                "created_at": offer.created_at,
            }
        )

    return offers_list


@router.get("/offer/{offer_uuid}/")
async def get_all_offer(
    offer_uuid: str, auth_user: interfaces.current_worker = Depends()
):

    offer = await services.OfferService().get_offer(
        offer_uuid=offer_uuid, user=auth_user
    )

    return {
        "offer_uuid": offer.offer_uuid,
        "user": offer.to_worker,
        "description": offer.description,
        "customer": offer.from_customer,
        "worker_has_read_it": offer.worker_has_read_it,
        "created_at": offer.created_at,
    }


@router.post("/{issue_uuid}/accept/", status_code=status.HTTP_201_CREATED)
async def accept_issue(
    issue_uuid: str, auth_user: interfaces.current_worker = Depends()
):

    await services.IssueTaskService().create_issue_task(
        issue_uuid=issue_uuid, user=auth_user
    )

    return {"detail": "You have accepted the issue"}


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
