import functools

from geopy import Nominatim


@functools.lru_cache
def get_locator_agent() -> Nominatim:
    return Nominatim(user_agent="esturide")
