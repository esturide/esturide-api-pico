import asyncio
import random
from typing import List

from fastapi import APIRouter

from app.core.exception import NotFoundException
from app.shared.const import DEFAULT_MAX_DELAY_TIME_SEARCH_LOCATION
from app.shared.dependencies import NominatimDepend, UserIsAuthenticated, AuthUserCodeAndRoleCredentials, \
    TrackingDependency
from app.shared.scheme import StatusResponse, StatusMessage
from app.shared.scheme.location import GeoLocationModel
from app.shared.types.enum import Status
from app.shared.utils import async_task

location_route = APIRouter(prefix="/location", tags=["Location address"])


@location_route.get("/search/{address}", response_model=StatusResponse[List[GeoLocationModel]])
async def search_location(address: str, geolocator: NominatimDepend, is_auth: UserIsAuthenticated):
    await asyncio.sleep(random.randint(*DEFAULT_MAX_DELAY_TIME_SEARCH_LOCATION))

    if is_auth:
        results = await async_task(
            lambda s: geolocator.geocode(s, exactly_one=False),
            address
        )

        if not results:
            raise NotFoundException(
                detail="No results were found for the specified address."
            )

        founds = []

        for locations in results:
            founds.append({
                "address": locations.address,
                "latitude": locations.latitude,
                "longitude": locations.longitude
            })

        return {
            "status": Status.success,
            "data": founds,
        }

    return {
        "status": Status.failure,
        "data": [],
    }


@location_route.post('/record')
async def record_location(tracking: TrackingDependency, location: GeoLocationModel,
                          user_auth: AuthUserCodeAndRoleCredentials) -> StatusMessage:
    code, role = user_auth

    return await tracking.register(code, role, location)
