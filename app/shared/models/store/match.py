import datetime
import uuid

from uuid import UUID

from aredis_om import JsonModel, Field

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.types import Seat, Gender


class MatchStore(JsonModel, index=True):
    pass
