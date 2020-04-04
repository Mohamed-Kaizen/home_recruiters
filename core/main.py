from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jobs import views as jobs_views
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from users import views as users_views

from .settings import settings
from .templates import html

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": settings.DB_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/rapidoc/")
async def rapi_doc():
    return HTMLResponse(html)


app.include_router(users_views.router, prefix="/users")
app.include_router(jobs_views.router, prefix="/jobs")
