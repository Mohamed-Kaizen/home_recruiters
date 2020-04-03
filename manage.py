from typing import Dict

import typer
import uvicorn
from core.settings import settings
from tortoise import Tortoise, run_async
from users import services

app = typer.Typer()


async def run(*, data: Dict):

    await Tortoise.init(
        db_url=settings.DATABASE_URL, modules={"models": settings.DB_MODELS}
    )

    await Tortoise.generate_schemas()

    await services.UserServices().create_super_user(data=data)


@app.command()
def serve():
    typer.echo("Running the server")
    uvicorn.run(
        "core.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug"
    )


@app.command()
def createuser():

    username = typer.prompt("Username")

    password = typer.prompt("Password")

    email = typer.prompt("Email")

    is_superuser = typer.confirm(f"is {username} super user?")

    is_staff = typer.confirm(f"is {username} staff user?")

    is_active = typer.confirm(f"is {username} active user?")

    run_async(
        run(
            data={
                "username": username,
                "password": password,
                "email": email,
                "full_name": " ",
                "is_superuser": is_superuser,
                "is_staff": is_staff,
                "is_active": is_active,
            }
        )
    )


if __name__ == "__main__":
    app()
