from users.depends import current_customer, current_worker
from users.services import UserServices


class UserInterfaces:
    @staticmethod
    async def get_user(*, username: str):

        user = await UserServices().get_worker(username=username)

        return user
