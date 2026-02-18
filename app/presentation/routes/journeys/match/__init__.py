import asyncio

from fastapi import APIRouter
from fastapi_sse import sse_handler

from app.shared.dependencies import AuthUserCodeAndRoleCredentials, MatchDependency, AsyncRedisDependency
from app.shared.scheme import StatusResponse, StatusMessage
from app.shared.scheme.match import MatchTravelRequest

match_router = APIRouter(prefix="/match", tags=["User Match System route"])


@match_router.get("/search", response_model=StatusResponse)
async def search_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    usercode, role = user_auth

    results = await match.search(usercode)

    if len(results) <= 0:
        return {
            "status": "failure",
            "data": []
        }

    return {
        "status": "success",
        "data": results
    }


@match_router.post("/", response_model=StatusMessage)
async def create_match(user_auth: AuthUserCodeAndRoleCredentials, travel: MatchTravelRequest, match: MatchDependency):
    usercode, role = user_auth

    return await match.create(usercode, travel.code)


@match_router.get("/status", response_model=StatusResponse)
@sse_handler()
async def status_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency, r: AsyncRedisDependency):
    usercode, role = user_auth

    async for status in match.check(usercode, r):
        yield status


@match_router.get('/', response_model=StatusResponse)
async def review_match(user_auth: AuthUserCodeAndRoleCredentials, match: MatchDependency):
    usercode, role = user_auth

    results = await match.review(usercode, role)

    if len(results) <= 0:
        return {
            "status": "failure",
            "data": []
        }

    return {
        "status": "success",
        "data": results
    }
