import contextlib
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.shared.types import Token


def create_oauth2_token(url="/auth/"):
    _oauth2_scheme = OAuth2PasswordBearer(url)

    def get_oauth2():
        return _oauth2_scheme

    return get_oauth2


get_oauth2_token = create_oauth2_token()


def encode(data: dict, expires_minutes: int, secret_key: str, algorithm: str) -> Token:
    payload = {
        **data,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode(token: Token, secret_key: str, algorithm: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def check_if_expired(token: Token, secret_key: str, algorithm: str) -> bool:
    try:
        decode(token, secret_key, algorithm)
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
