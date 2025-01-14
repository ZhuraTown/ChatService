from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, RedirectResponse

from common.exceptions import (
    ToClientException, IncorrectEmailOrPasswordException
)
from users.router import (users_router, users_api_router)
from chat.router import router as chat_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROUTES = [
    users_router,
    users_api_router,
    chat_router
]

for route in ROUTES:
    app.include_router(route)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(IncorrectEmailOrPasswordException)
async def incorrect_email_or_password_exception_handler(request: Request, exc: IncorrectEmailOrPasswordException):
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={"message": str(exc.message)},
    )


@app.exception_handler(ToClientException)
async def validation_exception_handler(request: Request, exc: ToClientException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"error": "Validation Error", "message": str(exc.message)},
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )