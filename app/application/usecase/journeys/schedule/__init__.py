import functools

from uuid import UUID
from typing import Optional

from fastapi import BackgroundTasks

from app.core.exception import InvalidRequestException, NotFoundException
from app.domain.service.auth import AuthenticationCredentialsService
from app.domain.service.background.listener import ListenerService
from app.domain.service.location.route import RouteService
from app.domain.service.location.search import SearchService
from app.domain.service.journeys.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.dependencies.depends import GoogleMapsClient
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.user import UserDocument
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest, DriverUser
from app.shared.types.enum import RoleUser


class ScheduleListenerService(ListenerService):
    def __init__(self, schedule: ScheduleStore) -> None:
        self.__schedule = schedule

    async def task(self):
        pass


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = ScheduleTravelService()
        self.user_service = UserService()
        self.auth_service = AuthenticationCredentialsService()

    async def create(self, req: ScheduleTravelFromAddressRequest, code: int, role: RoleUser, gmaps: GoogleMapsClient):
        search_service = SearchService(gmaps)
        route_service = RouteService(gmaps)

        if role != RoleUser.driver:
            raise InvalidRequestException('Role must be driver.')

        user = await self.user_service.get(code)

        if user is None:
            raise NotFoundException('User does not exist.')

        origin_results = await search_service.search(req.origin)
        destination_results = await search_service.search(req.destination)

        origin = origin_results[0]
        destination = destination_results[0]
        starting = req.starting

        route_results = await route_service.routing(origin.address, destination.address, req.waypoints, starting)
        route_steps = route_results[0].steps

        schedule = await self.schedule_service.create(
            user=user,
            origin=origin.address,
            destination=destination.address,
            starting=starting,
            price=req.price,
            seats=req.seats,
            genders=req.genders,
            waypoints=req.waypoints,
            route=route_steps,
        )

        if schedule is None:
            return StatusFailure(
                message="The trip could not be scheduled."
            )

        return StatusSuccess(
            message="New travel traveled successfully."
        )

    async def exist(self, usercode: int) -> bool:
         schedule = await self.schedule_service.get_from_user(usercode)

         return schedule is not None

    async def current(self, usercode: int, role: RoleUser) -> ScheduleTravelResponse | None:
        if role != RoleUser.driver:
            return None

        schedule = await self.schedule_service.get_from_user(usercode)

        if schedule is None:
            return None

        return ScheduleTravelResponse(
            code=schedule.usercode,
            starting=schedule.starting,
            price=schedule.price,
            origin=schedule.origin,
            destination=schedule.destination,
            genders=schedule.genders,
            waypoints=schedule.waypoints
        )


@functools.lru_cache
def get_schedule_use_case():
    return ScheduleTravelUseCase()
