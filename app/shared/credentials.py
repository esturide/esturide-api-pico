from typing import Annotated

from fastapi import Depends, HTTPException

from app.core import get_settings
from app.core.oauth2 import oauth2_scheme, secure_decode, decode
from app.shared.models.user import User
from app.shared.types import Token
from app.shared.types.enum import RoleUser


async def user_credentials(token: Annotated[Token, Depends(oauth2_scheme)]) -> int | None:
    settings = get_settings()

    if token is None:
        return None

    with secure_decode(token, settings.secret_key, settings.algorithm) as decoded:
        if code := decoded.get("code"):
            return code
        else:
            raise None


async def get_user_code_from_credentials(token: Annotated[Token, Depends(oauth2_scheme)]) -> int:
    settings = get_settings()

    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    with secure_decode(token, settings.secret_key, settings.algorithm) as decoded:
        if code := decoded.get("code"):
            return code
        else:
            raise HTTPException(status_code=401, detail="Not authenticated.")


async def get_user_code_and_role_code_from_credentials(token: Annotated[Token, Depends(oauth2_scheme)]) -> tuple[
    int, RoleUser]:
    settings = get_settings()

    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    data_decode = decode(token, settings.secret_key, settings.algorithm)

    return data_decode['code'], RoleUser(data_decode['role'])


async def is_user_authenticated(token: Annotated[Token, Depends(oauth2_scheme)]) -> bool:
    settings = get_settings()

    if token is None:
        return False

    with secure_decode(token, settings.secret_key, settings.algorithm) as decoded:
        if decoded.get("code") is not None:
            return True

    return False


async def get_user_credentials_header(headers) -> User | None:
    if access_token := headers.get("access_token"):
        return await user_credentials(access_token)

    if access_token := headers.get("accessToken"):
        return await user_credentials(access_token)

    return None
