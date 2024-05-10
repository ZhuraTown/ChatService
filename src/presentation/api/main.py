from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from beanie import init_beanie
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient

from starlette.exceptions import ExceptionMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from application.common.exceptions import ToClientException
from log import app_logger
from presentation.api.middlewares.logging import RequestLogMiddleware
from src.infrastructure.db.models import User
from src.presentation.api.controllers.user import router as user_router
from src.presentation.api.config import api_settings

from src.config import settings


MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(RequestLogMiddleware),
]


@asynccontextmanager
async def lifespan_init_db(app: FastAPI):
    client = AsyncIOMotorClient(str(settings.infrastructure.mongo_dsn))
    await init_beanie(client.chat, document_models=[User])
    yield

app = FastAPI(title="chat", version="1.0.0", middleware=MIDDLEWARES, lifespan=lifespan_init_db)


@app.exception_handler(ToClientException)
async def bad_request_handler(request: Request,  exc: ToClientException):
    app_logger.error(f"Exception - {exc.__class__.__name__}, Detail - {exc.message}")
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"error": "Client Error", "message": str(exc.message)},
    )

app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)


ROUTERS = [
    user_router,
]

for router in ROUTERS:
    app.include_router(router)


def main():
    print("FastAPI starting...")
    # app_logger.info("FastAPI starting...")
    uvicorn.run(
        "presentation.api.main:app",
        host=api_settings.HOST,
        port=api_settings.PORT,
        reload=api_settings.RELOAD,
        workers=api_settings.WORKERS,
        log_level="warning",
    )


if __name__ == "__main__":
    main()