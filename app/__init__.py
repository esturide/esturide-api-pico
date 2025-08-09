import functools

from geopy.geocoders import Nominatim
from fastapi import HTTPException
from jwt import InvalidSignatureError

from app.config import get_settings
from app.core import get_root_app
from app.routes import router_app
from app.routes.user import user_router
from app.core.exception import ResponseException
from app.core.exception.handler import custom_http_exception_handler, http_exception_handler, \
    invalid_credentials_handler, global_exception_handler


@functools.lru_cache
def get_app():
    app = get_root_app()

    app.add_exception_handler(ResponseException, custom_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(router_app)
    app.include_router(user_router)

    return app
