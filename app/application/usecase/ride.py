import functools


class RideUseCase:
    pass


@functools.lru_cache
def ger_ride_use_case():
    return RideUseCase()
