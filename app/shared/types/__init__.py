import typing
import uuid

from fastapi import UploadFile

from app.shared.types.enum import Gender
from app.shared.types.enum.seats import Seats

UserType = typing.TypeVar("UserType")
M = typing.TypeVar('M')

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
UUID = typing.TypeVar("UUID", str, uuid.UUID)
Token = typing.TypeVar("Token", str, bytes)

StatusQuery = typing.Tuple[bool, typing.AnyStr]

SeatList = typing.Set[Seats]
GenderList = typing.Set[Gender]
