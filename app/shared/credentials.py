from typing import Annotated

from fastapi import Depends, HTTPException

from app.core.oauth2 import oauth2_scheme, secure_decode
from app.infrestructure.repository.user import UserRepository
from app.shared.models.user import User
from app.shared.types import Token


async def user_credentials(token: Annotated[Token, Depends(oauth2_scheme)]) -> User | None:
    if token is None:
        return None

    with secure_decode(token) as decoded:
        if code := decoded.get("code"):
            return await UserRepository.get_user_by_code(code)
        else:
            raise None


async def user_is_authenticated(token: Annotated[Token, Depends(oauth2_scheme)]) -> int | None:
    user = await user_credentials(token)

    if user is not None:
        return user.code

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def get_user_is_authenticated(token: Annotated[Token, Depends(oauth2_scheme)]) -> User:
    user = await user_credentials(token)

    if user is not None:
        return user

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def validate_admin_role(token: Annotated[Token, Depends(oauth2_scheme)]) -> bool | None:
    user = await user_credentials(token)

    if user is not None:
        return user.is_admin

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def validate_permission_role(token: Annotated[Token, Depends(oauth2_scheme)]) -> bool | None:
    result, user = await user_credentials(token)

    if user is not None:
        return user.is_admin or user.is_staff

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def get_user_credentials_header(headers) -> User | None:
    if access_token := headers.get("access_token"):
        return await user_credentials(access_token)

    if access_token := headers.get("accessToken"):
        return await user_credentials(access_token)

    return None
