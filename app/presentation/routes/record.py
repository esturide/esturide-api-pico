from fastapi import APIRouter

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, TrackingDependency
from app.shared.scheme import StatusMessage
from app.shared.scheme.location import GeoLocationModel

record_route = APIRouter(prefix="/record", tags=["Record tracking route"])


@record_route.post('/')
async def record_location(tracking: TrackingDependency, location: GeoLocationModel,
                          user_auth: AuthUserCodeAndRoleCredentials) -> StatusMessage:
    code, role = user_auth

    return await tracking.register(code, role, location)
