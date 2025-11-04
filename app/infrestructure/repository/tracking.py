from app.infrestructure.repository.client.db import ClientDocumentRepository
from app.shared.pattern.singleton import Singleton


class TrackingRepository(ClientDocumentRepository, metaclass=Singleton):
    pass
