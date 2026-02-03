from fastapi import APIRouter

from app.shared.dependencies import OAuth2Scheme, AuthDependency, ScheduleDependency
from app.shared.scheme import StatusResponse
from app.shared.types.enum import Status, CurrentSession, RoleUser

find_router = APIRouter(prefix="/find", tags=["Find route"])

@find_router.get('/status', response_model=StatusResponse[CurrentSession])
async def find_current_status(token: OAuth2Scheme, auth: AuthDependency, schedule_case: ScheduleDependency):
    user, role = await auth.get_current_status(token)
    schedule = await schedule_case.get_current(user.code)

    sessions = {
        RoleUser.driver: CurrentSession.travel,
        RoleUser.passenger: CurrentSession.ride,
    }

    return {
        "status": Status.success,
        "data": sessions[role]
    }
