import asyncio

from fastapi import APIRouter
from fastapi_sse import sse_handler

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, MatchDependency
from app.shared.scheme import StatusResponse
from app.shared.scheme.rides.status import CurrentRideStatus

match_router = APIRouter(prefix="/match", tags=["User Match System route"])


@match_router.get("/search", response_model=StatusResponse)
async def search_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    await match.search()


@match_router.get("/status", response_model=StatusResponse)
@sse_handler()
async def status_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    for _ in range(30):
        yield CurrentRideStatus()

        await asyncio.sleep(1)
