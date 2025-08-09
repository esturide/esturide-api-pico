import contextlib
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings
from app.types import Token


def create_oauth2_token(url="/auth/"):
    _oauth2_scheme = OAuth2PasswordBearer(url)

    def get_oauth2():
        return _oauth2_scheme

    return get_oauth2


get_oauth2_token = create_oauth2_token()


def encode(data: dict, expires_minutes: int) -> Token:
    settings = get_settings()
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)

    data_to_encode.update({
        "exp": expire
    })

    return jwt.encode(data_to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode(token: Token) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def check_if_expired(token: Token) -> bool:
    try:
        decode(token)
    except jwt.ExpiredSignatureError:
        return False
    finally:
        return True


@contextlib.contextmanager
def secure_decode(token: Token):
    try:
        yield decode(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials.",
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Signature verification failed.",
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid token.",
        )


def get_code_from_token(token: Token) -> int:
    with secure_decode(token) as decoded:
        if code := decoded.get("code"):
            return code


oauth2_scheme = get_oauth2_token()
