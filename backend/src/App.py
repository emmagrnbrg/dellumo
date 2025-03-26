from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from .errors.ValidationError import ValidationError
from .routers import RegistrationRouter, OperationRouter, ResetPasswordRouter, AuthorizationRouter, UserRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validationExceptionHandler(request: Request, e: RequestValidationError):
    raise ValidationError(e.errors()[0]["loc"][1])

app.include_router(RegistrationRouter.router)
app.include_router(OperationRouter.router)
app.include_router(ResetPasswordRouter.router)
app.include_router(AuthorizationRouter.router)
app.include_router(UserRouter.router)
