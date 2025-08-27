from typing import List

from fastapi import APIRouter

from app.core.exception import NotFoundException
from app.shared.dependencies import NominatimDepend, UserIsAuthenticated
from app.shared.scheme import StatusResponse
from app.shared.scheme.location import GeoLocationModel, GeoLocationResultResponse, LocationAddressModel
from app.shared.types.enum import Status
from app.shared.utils import async_task

location_route = APIRouter(prefix="/location", tags=["Location address"])


@location_route.post("/search", response_model=StatusResponse[List[GeoLocationResultResponse]])
async def search_address(search: LocationAddressModel, geolocator: NominatimDepend, is_auth: UserIsAuthenticated):
    if is_auth:
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

    return {
        "status": Status.failure,
        "data": [],
    }


@location_route.post("/reverse", response_model=StatusResponse[LocationAddressModel])
async def search_address(location: GeoLocationModel, geolocator: NominatimDepend, is_auth: UserIsAuthenticated):
    if is_auth:
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
            "data": { "address": results.address },
        }

    return {
        "status": Status.failure,
            "data": { "address": "" },
    }
