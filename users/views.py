from typing import Any, Dict

from core.settings import settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from tortoise.contrib.fastapi import HTTPNotFoundError

from . import schema, services, utils, models, interfaces

router = APIRouter()


@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:

    user = await services.UserServices().authenticate(
        username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = utils.create_access_token(
        data={"sub": user.username, "user_uuid": f"{user.user_uuid}"},
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/",
    description="Get ALL Users",
    response_description="List of users",
    response_model=schema.UserList,
)
async def list_of_all_users():

    users = await services.UserServices().get_all_users()

    return schema.UserList(username=[f"{user}" for user in users])


@router.get(
    "/customers/",
    description="Get ALL Customers",
    response_description="List of customers",
    response_model=schema.UserList,
)
async def list_of_customers():

    users = await services.UserServices().get_all_customers()

    return schema.UserList(username=[f"{user}" for user in users])


@router.post(
    "/customers/",
    status_code=status.HTTP_201_CREATED,
    description="Creating New Customers",
)
async def add_customer(user_input: schema.CustomerCreate) -> Dict[str, Any]:

    user = await services.UserServices().create_customer(user=user_input)

    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_customer": user.is_customer,
        "phone_number": user.phone_number,
    }


@router.get(
    "/workers/",
    description="Get ALL Workers",
    response_description="List of workers",
    response_model=schema.UserList,
)
async def list_of_workers():

    users = await services.UserServices().get_all_workers()

    return schema.UserList(username=[f"{user}" for user in users])


@router.post(
    "/workers/",
    status_code=status.HTTP_201_CREATED,
    description="Creating New Workers",
)
async def add_worker(user_input: schema.WorkerCreate) -> Dict[str, Any]:

    user = await services.UserServices().create_worker(user=user_input)

    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_worker": user.is_worker,
        "phone_number": user.phone_number,
        "career": user.career,
    }


@router.get("/workers/{username}/task/")
async def get_worker_tasks(username: str):
    return await interfaces.IssueTaskInterfaces().get_all_issue_task(username=username)


@router.get(
    "/workers/{username}/",
    response_model=models.User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_worker(username: str):
    return await services.UserServices().get_worker_by_username(username=username)
