from fastapi import APIRouter
from passlib.context import CryptContext

from app.shared.dependencies import OAuth2Form, AuthDependency, OAuth2Scheme
from app.shared.scheme import StatusMessage, StatusResponse
from app.shared.scheme.auth import AccessCredentialForm, AccessLogin, AccessCredential
from app.shared.types.enum import Status

auth_route = APIRouter(
    prefix="/auth",
    tags=["Auth router"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_route.post("/", response_model=AccessCredentialForm)
async def login_from_form(form: OAuth2Form, auth: AuthDependency):
    code = form.username
    password = form.password

    token = await auth.login(code, password)

    return {
        "access_token": token,
    }


@auth_route.post("/login", response_model=AccessCredential)
async def login(access: AccessLogin, auth: AuthDependency):
    token = await auth.login(access.username, access.password.get_secret_value())

    return {
        "token": token,
    }


@auth_route.post("/check", response_model=StatusMessage)
async def check_token(token: OAuth2Scheme, auth: AuthDependency):
    status = await auth.check(token)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
    }


@auth_route.post("/refresh", response_model=StatusResponse[AccessCredential])
async def refresh_token(token: OAuth2Scheme, auth: AuthDependency):
    token = await auth.refresh(token)

    return {
        "status": Status.success,
        "data": AccessCredential(
            token=token,
        )
    }
