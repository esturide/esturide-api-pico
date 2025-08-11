import typing
import uuid

from fastapi import UploadFile

UserType = typing.TypeVar("UserType")
M = typing.TypeVar('M')

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
UUID = typing.TypeVar("UUID", str, uuid.UUID)
Token = typing.TypeVar("Token", str, bytes)

StatusQuery = typing.Tuple[bool, typing.AnyStr]
