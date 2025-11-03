from app.infrestructure.repository.session import AsyncSessionRepository
from app.shared.pattern.singleton import Singleton


class TrackingRepository(AsyncSessionRepository, metaclass=Singleton):
    pass
