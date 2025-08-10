import asyncio
import random
from typing import List

from fastapi import APIRouter

from app.core.exception import NotFoundException
from app.shared.dependencies import NominatimDepend
from app.shared.scheme.location import DataGeoLocation
from app.shared.utils import async_task

location_route = APIRouter(prefix="/location", tags=["Location address"])


@location_route.get("/search/{address}", response_model=List[DataGeoLocation])
async def search_location(address: str, geolocator: NominatimDepend):
    await asyncio.sleep(random.randint(1, 5))

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

    return founds
