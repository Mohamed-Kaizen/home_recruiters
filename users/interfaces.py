from typing import List

from jobs.models import IssueTask


class IssueTaskInterfaces:

    @staticmethod
    async def get_all_issue_task(*, username: str) -> List[IssueTask]:

        return await IssueTask.filter(worker=username)
