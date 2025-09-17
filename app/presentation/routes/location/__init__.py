import asyncio
import random
from typing import List

from fastapi import APIRouter

from app.core.exception import NotFoundException
from app.shared.dependencies import UserIsAuthenticated, GoogleGeolocationDepend
from app.shared.scheme import StatusResponse
from app.shared.scheme.location import GeoLocationModel, GeoLocationAddressModel, LocationAddressModel
from app.shared.types.enum import Status
from app.shared.utils import async_task

location_route = APIRouter(prefix="/location", tags=["Location address"])


@location_route.post("/search", response_model=StatusResponse[List[GeoLocationAddressModel]])
async def search_address(search: LocationAddressModel, geolocator: GoogleGeolocationDepend,
                         is_auth: UserIsAuthenticated):
    if not is_auth:
        return {
            "status": Status.failure,
            "data": [],
        }

    await asyncio.sleep(random.randint(1, 3))

    address = search.address

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


@location_route.post("/reverse", response_model=StatusResponse[LocationAddressModel])
async def search_address(location: GeoLocationModel, geolocator: GoogleGeolocationDepend, is_auth: UserIsAuthenticated):
    if not is_auth:
        return {
            "status": Status.failure,
            "data": {"address": ""},
        }

    await asyncio.sleep(random.randint(1, 3))

    coords = (location.latitude, location.longitude)

    results = await async_task(
        geolocator.reverse,
        coords
    )

    if not results:
        raise NotFoundException(
            detail="No results were found for the specified geolocation."
        )

    return {
        "status": Status.success,
        "data": {"address": results.address},
    }
