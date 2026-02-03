import typing

from fastapi import UploadFile

from app.shared.types.enum import Gender
from app.shared.types.enum.seats import Seat

UserType = typing.TypeVar("UserType")
M = typing.TypeVar('M')

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
Token = typing.TypeVar("Token", str, bytes)

StatusQuery = typing.Tuple[bool, typing.AnyStr]

SeatOption = typing.Set[Seat]
GenderOption = typing.Set[Gender]
