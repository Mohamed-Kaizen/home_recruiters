from typing import List

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Home Recruiters"

    PROJECT_DESCRIPTION: str = """
    Every person needs help from other professionals be it electricians, plumbers, mechanics or any other.
     This project is a quick and easy way for people(recruiters) to connect with skilled people
      who think are a good fit and hire them
     """

    PROJECT_VERSION: str = "0.1.0"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    ALLOWED_HOSTS: List[str] = ["127.0.0.1", "localhost"]

    DEBUG: bool

    SECRET_KEY: str

    DATABASE_URL: str = "sqlite://./db.sqlite3"

    DB_MODELS: List[str] = ["users.models", "jobs.models"]

    CORS_ORIGINS: List[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    CORS_ALLOW_METHODS: List[str] = ["*"]

    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Don't decrease this number unless you have a good reason not to.
    # Please read
    # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#maximum-password-lengths
    MINIMUM_PASSWORD_LENGTH: int = 8

    # Don't increase this number unless you have a good reason not to.
    # Please read
    # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#maximum-password-lengths
    MAXIMUM_PASSWORD_LENGTH: int = 16

    PASSWORD_CONTEXT: None = CryptContext(schemes=["bcrypt"], deprecated="auto")

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/users/login/")

    User_MODEL: str = "users.models.User"

    class Config:
        env_file = ".env"


settings = Settings()
