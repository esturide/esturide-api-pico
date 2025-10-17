import functools

from app.shared.pattern.singleton import Singleton


class MatchUseCase(metaclass=Singleton):
    def __init__(self):
        pass

    async def search(self):
        pass

    async def accept(self):
        pass


@functools.lru_cache
def get_match_use_case():
    return MatchUseCase()
