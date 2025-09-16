import functools

from geopy.geocoders import GoogleV3, Nominatim
from app.core import get_settings


@functools.lru_cache
def get_nominatim_locator_agent() -> Nominatim:
    return Nominatim(user_agent="esturide")


@functools.lru_cache
def get_google_locator_agent() -> GoogleV3:
    settings = get_settings()

    return GoogleV3(api_key=settings.api_google_geolocation_key)
