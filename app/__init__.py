import functools

from fastapi import HTTPException
from jwt import InvalidSignatureError

from app.core import get_root_app
from app.core.exception import ResponseException
from app.core.exception.handler import (custom_http_exception_handler, http_exception_handler, \
                                        invalid_credentials_handler, global_exception_handler)
from app.presentation.routes import root_router
from app.presentation.routes.auth import auth_route
from app.presentation.routes.location import location_route
from app.presentation.routes.schedule import schedule_router
from app.presentation.routes.user import user_router


@functools.lru_cache
def get_app():
    app = get_root_app()

    app.add_exception_handler(ResponseException, custom_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(root_router)
    app.include_router(auth_route)
    app.include_router(location_route)
    app.include_router(schedule_router)
    app.include_router(user_router)

    return app
