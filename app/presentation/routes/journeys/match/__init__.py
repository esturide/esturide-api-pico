import asyncio

from uuid import UUID

from fastapi import APIRouter
from fastapi_sse import sse_handler

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, MatchDependency
from app.shared.scheme import StatusResponse, StatusMessage

match_router = APIRouter(prefix="/match", tags=["User Match System route"])


@match_router.get("/search", response_model=StatusResponse)
async def search_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    usercode, role = user_auth

    results = await match.search(usercode)

    if len(results) <= 1:
        return {
            "status": "failure",
            "data": []
        }

    return {
        "status": "success",
        "results": results
    }


@match_router.post("/create", response_model=StatusMessage)
async def create_match(user_auth: AuthUserCodeAndRoleCredentials, travel_schedule_id: UUID, match: MatchDependency):
    usercode, role = user_auth

    return await match.create(usercode, travel_schedule_id)


@match_router.get("/status", response_model=StatusResponse)
@sse_handler()
async def status_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    usercode, role = user_auth

    async for status in match.check(usercode):
        yield status

        await asyncio.sleep(1)
