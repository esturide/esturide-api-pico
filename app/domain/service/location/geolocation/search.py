from typing import Tuple

from geopy.geocoders.base import Geocoder

from app.shared.utils import async_task


async def search_location_from_address(geocoder: Geocoder, address: str, country: str = "MX") -> list[
    Tuple[str, Tuple[float, float]]]:
    component_restrictions = {
        "country": country
    }

    results = await async_task(
        lambda s: geocoder.geocode(
            s,
            exactly_one=False,
            components=component_restrictions
        ),
        address
    )

    if not results:
        return []

    founds = []

    for locations in results:
        founds.append(
            (locations.address, (locations.latitude, locations.longitude))
        )

    return founds
