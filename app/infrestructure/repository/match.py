from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.shared.pattern.singleton import Singleton


class MatchRepository(ClientCacheRepository, metaclass=Singleton):
    pass
