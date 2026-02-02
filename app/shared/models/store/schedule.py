import base64
import datetime

from typing import Annotated, Any, Tuple, List, Set

import numpy as np
import zlib

from aredis_om import JsonModel, Field
from pydantic import BeforeValidator, AfterValidator, ValidationError

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.types import Seat, Gender


def encode_route(route: List[Tuple[float, float]] | Any) -> str:
    if isinstance(route, list):
        return base64.b64encode(np.array(route, dtype=np.float32).tobytes()).decode()

    raise ValidationError("Invalid decode route.")


def decode_route(route: str) -> List[Tuple[float, float]]:
    if isinstance(route, str):
        return np.frombuffer(base64.b64decode(route), dtype=np.float32).reshape(-1, 2).tolist()

    raise ValidationError("Invalid decode route.")


def encode_compress_route(route: List[Tuple[float, float]] | Any) -> str:
    if isinstance(route, list):
        encode_arr = np.array(route, dtype=np.float32).tobytes()
        compress_arr = zlib.compress(encode_arr, level=9)

        return base64.b64encode(compress_arr).decode()

    raise ValidationError("Invalid decode route.")


def decode_compress_route(route: str) -> List[Tuple[float, float]]:
    if isinstance(route, str):
        decode_arr = base64.b64decode(route)
        decompress_arr = zlib.decompress(decode_arr)

        return np.frombuffer(decompress_arr, dtype=np.float32).reshape(-1, 2).tolist()

    raise ValidationError("Invalid decode route.")


EncodeRoute = Annotated[str, BeforeValidator(encode_compress_route), AfterValidator(decode_compress_route)]


class ScheduleStore(JsonModel, index=True):
    usercode: int = Field(..., index=True, const=True)
    created: datetime.datetime = Field(default_factory=datetime.datetime.now, index=True, const=True)

    origin: str = Field(..., index=True, const=True, full_text_search=True)
    destination: str = Field(..., index=True, const=True, full_text_search=True)

    starting: datetime.datetime = Field(..., index=True, const=True)

    price: float = Field(index=True, const=True)
    seats: Set[Seat] = Field(default_factory=set)
    genders: Set[Gender] = Field(default_factory=set)

    waypoints: Set[str] = Field(..., default_factory=set, const=True)
    route: EncodeRoute = Field(..., index=False, const=True)

    class Meta:
        database = get_async_client_redis()
