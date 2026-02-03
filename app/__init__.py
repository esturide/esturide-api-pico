import functools

from fastsio import ASGIApp
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from jwt import InvalidSignatureError

from app.core import get_root_app
from app.core.exception import ResponseException
from app.core.exception.handler import (custom_http_exception_handler, http_exception_handler, \
                                        invalid_credentials_handler, global_exception_handler,
                                        validation_exception_handler, database_exception_handler,
                                        not_implemented_handler)
from app.presentation.routes import root_router
from app.presentation.routes.auth import auth_route
from app.presentation.routes.check import find_router
from app.presentation.routes.location import location_route
from app.presentation.routes.notify import notify_route
from app.presentation.routes.record import record_route
from app.presentation.routes.rides import rides_router
from app.presentation.routes.rides.match import match_router
from app.presentation.routes.rides.socket import ride_sio
from app.presentation.routes.schedule import schedule_router
from app.presentation.routes.schedule.socket import travel_sio
from app.presentation.routes.user import user_router
from app.shared.dependencies.depends.socketio import get_root_socketio_server


@functools.lru_cache
def get_app():
    app = get_root_app()
    sio = get_root_socketio_server()

    app.add_exception_handler(NotImplementedError, not_implemented_handler)
    app.add_exception_handler(ResponseException, custom_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(root_router)
    app.include_router(auth_route)
    app.include_router(user_router)
    app.include_router(match_router)
    app.include_router(schedule_router)
    app.include_router(rides_router)
    app.include_router(notify_route)
    app.include_router(location_route)
    app.include_router(record_route)
    app.include_router(find_router)

    app = ASGIApp(sio, app)
    sio.add_router(ride_sio)
    sio.add_router(travel_sio)

    return app
