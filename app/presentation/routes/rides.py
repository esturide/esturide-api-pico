from fastapi import APIRouter, BackgroundTasks

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, RideDependency
from app.shared.scheme import StatusResponse, StatusMessage
from app.shared.scheme.rides import RideTravelUpdateRequest, RideTravelRequest
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types.enum import Status

rides_router = APIRouter(prefix="/rides", tags=["Rides"])


@rides_router.post('/')
async def request_new_ride(req: RideTravelRequest, user_auth: AuthUserCodeAndRoleCredentials,
                           ride: RideDependency, background_tasks: BackgroundTasks) -> StatusMessage:
    code, role = user_auth

    return await ride.create(code, role, req, background_tasks)


@rides_router.get('/', response_model=StatusResponse[RideTravelStatusResponse])
async def get_current_ride(user_auth: AuthUserCodeAndRoleCredentials, ride: RideDependency):
    code, role = user_auth
    data = await ride.current(code)

    return StatusResponse(
        status=Status.success,
        data=data
    )


@rides_router.post('/update')
async def update_ride(req: RideTravelUpdateRequest, user_auth: AuthUserCodeAndRoleCredentials,
                      ride: RideDependency) -> StatusMessage:
    code, role = user_auth

    return await ride.update(req, code, role)
