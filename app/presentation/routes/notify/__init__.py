from fastapi import APIRouter
from fastapi_sse import sse_handler
from starlette.responses import StreamingResponse

from app.shared.dependencies import NotifyDependency, AuthUserCodeAndRoleCredentials
from app.shared.scheme import StatusResponse
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types.enum import Status

notify_route = APIRouter(
    prefix="/notify",
    tags=["Notification System route"]
)


@notify_route.get("/ride")
@sse_handler()
async def notify_ride_status(notify: NotifyDependency, user_auth: AuthUserCodeAndRoleCredentials):
    code, role = user_auth

    async for data in notify.notify_ride(code, role):
        yield StatusResponse(
            status=Status.success,
            data=data,
        )



@notify_route.get("/schedule")
@sse_handler()
async def notify_ride_status(notify: NotifyDependency, user_auth: AuthUserCodeAndRoleCredentials):
    code, role = user_auth

    async for data in notify.notify_schedule(code, role):
        yield StatusResponse(
            status=Status.success,
            data=data,
        )

