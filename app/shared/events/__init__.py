import typing

from fastsio import SocketID, AsyncServer

DataMessage = typing.TypeVar("DataMessage")


class AsyncSocketEmitter(typing.Generic[DataMessage]):
    def __init__(self, server: AsyncServer, namespace: str = "/", sid: typing.Optional[SocketID] = None):
        self.__server = server
        self.__namespace = namespace
        self.__sid = sid

    async def send(self, event: str, data: DataMessage, to: typing.Optional[SocketID] = None):
        target = to or self.__sid
        await self.__server.emit(event, data, namespace=self.__namespace, to=target)

    async def broadcast(self, event: str, data: DataMessage, room: typing.Optional[SocketID] = None):
        await self.__server.emit(event, data, namespace=self.__namespace, room=room)
