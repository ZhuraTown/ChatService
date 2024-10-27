import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.config import settings

from src.users.routes import router as user_router


MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    # Middleware(RequestLogMiddleware),
    # Middleware(ClientMiddleware),
]

ROUTES = [
    user_router,
]

app = FastAPI(
    title='chat_service',
)


for route in ROUTES:
    app.include_router(user_router)


def start_api_server():
    uvicorn.run(
        "src.main:app",
        host=settings.api_settings.API_HOST,
        port=settings.api_settings.API_PORT,
        reload=settings.api_settings.API_RELOAD,
        workers=settings.api_settings.API_WORKERS,
        log_level="warning",
    )


if __name__ == "__main__":
    print(f"Server started: {settings.api_settings.API_HOST}:{settings.api_settings.API_PORT}")
    print(f"Is debug: {settings.debug}")
    start_api_server()
