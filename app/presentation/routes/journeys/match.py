from fastapi import APIRouter

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, MatchDependency
from app.shared.scheme import StatusResponse
from app.shared.scheme.rides import RideTravelRequest

match_router = APIRouter(prefix="/match", tags=["User Match System route"])


@match_router.get("/search", response_model=StatusResponse)
async def search_match(req: RideTravelRequest, user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    await match.search()


@match_router.post("/accept", response_model=StatusResponse)
async def accept_match(req: RideTravelRequest, user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    await match.accept()
