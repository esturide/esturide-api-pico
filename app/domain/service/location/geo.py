from geopy.geocoders.base import Geocoder

from app.shared.scheme.location import GeoLocationModel, GeoLocationAddressModel
from app.shared.utils import async_task


async def search_from_address(geocoder: Geocoder, address: str) -> list[GeoLocationAddressModel]:
    results = await async_task(
        lambda s: geocoder.geocode(s, exactly_one=False),
        address
    )

    if not results:
        return []

    founds = []

    for locations in results:
        founds.append(GeoLocationAddressModel(
            latitude=locations.latitude,
            longitude=locations.longitude,
            address=locations.address
        ))

    return founds


async def reverse_search_from_location(geocoder: Geocoder, location: GeoLocationModel) -> list[GeoLocationAddressModel]:
    coords = (location.latitude, location.longitude)

    results = await async_task(
        geocoder.reverse,
        coords
    )

    if not results:
        return []

    founds = []

    for locations in results:
        founds.append(GeoLocationAddressModel(
            latitude=locations.latitude,
            longitude=locations.longitude,
            address=locations.address
        ))

    return founds
