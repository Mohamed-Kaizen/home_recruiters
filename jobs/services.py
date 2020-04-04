from typing import List

from fastapi import HTTPException, status
from tortoise import exceptions as tortoise_exceptions

from .interfaces import UserInterfaces
from .models import Issue, Issue_Pydantic, Offer
from .schema import CreateIssue, CreateOffer


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


class OfferService:
    @staticmethod
    async def create_offer(*, offer: CreateOffer, user) -> Offer:

        worker = await UserInterfaces().get_user(username=offer.username)

        offer = await Offer.create(
            from_customer=user.username,
            description=offer.description,
            to_worker=worker.username,
        )

        return offer

    @staticmethod
    async def get_offers(*, user) -> List[Offer]:

        return await Offer.filter(to_worker=user.username)

    @staticmethod
    async def get_offer(*, offer_uuid: str, user) -> Offer:

        offer = await Offer.get(offer_uuid=offer_uuid, to_worker=user.username)

        offer.worker_has_read_it = True

        await offer.save()

        return offer
