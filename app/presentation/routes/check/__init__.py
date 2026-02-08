from fastapi import APIRouter

from app.shared.dependencies import OAuth2Scheme, AuthDependency, ScheduleDependency, RideDependency
from app.shared.scheme import StatusResponse
from app.shared.scheme.status import UserStatus
from app.shared.types.enum import Status, CurrentSession, RoleUser

check_router = APIRouter(prefix="/find", tags=["Find route"])

@check_router.get('/status', response_model=StatusResponse[UserStatus])
async def find_current_status(token: OAuth2Scheme, auth: AuthDependency, schedule_case: ScheduleDependency, ride_case: RideDependency):
    sessions = {
        RoleUser.driver: CurrentSession.travel,
        RoleUser.passenger: CurrentSession.ride,
    }

    user, role = await auth.get_current_status(token)
    schedule = await schedule_case.exist(user.code)
    ride = await ride_case.exist(user.code)

    current_session = CurrentSession.free

    if not (schedule or ride):
        return {
            "status": Status.success,
            "data": {
                "session": current_session,
                "role": role
            }
        }

    if schedule:
        current_session = CurrentSession.travel
    elif ride:
        current_session = CurrentSession.ride

    return {
        "status": Status.success,
        "data": {
            "session": current_session,
            "role": role
        }
    }
