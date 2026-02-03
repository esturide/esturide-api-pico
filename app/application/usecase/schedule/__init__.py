import functools
from typing import Optional

from fastapi import BackgroundTasks

from app.core.exception import InvalidRequestException, NotFoundException
from app.domain.service.auth import AuthenticationCredentialsService
from app.domain.service.background.listener import ListenerService
from app.domain.service.location.route import RouteService
from app.domain.service.location.search import SearchService
from app.domain.service.schedule import ScheduleService
from app.domain.service.user import UserService
from app.shared.dependencies.depends import GoogleMapsClient
from app.shared.models.store.schedule import ScheduleStore
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.location import GeoPoint
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest, DriverUser
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import RoleUser


class ScheduleListenerService(ListenerService):
    def __init__(self, schedule: ScheduleStore) -> None:
        self.__schedule = schedule

    async def task(self):
        pass


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = ScheduleService()
        self.user_service = UserService()
        self.auth_service = AuthenticationCredentialsService()

    async def create(self, req: ScheduleTravelFromAddressRequest, code: int, role: RoleUser, gmaps: GoogleMapsClient,
                     background_tasks: BackgroundTasks):
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

        """
        schedules_task = ScheduleTaskService(cache)
        schedules_task.create_task(background_tasks, schedule)
        """

        if schedule is None:
            return StatusFailure(
                message="The trip could not be scheduled."
            )

        return StatusSuccess(
            message="New travel traveled successfully."
        )

    async def find_schedule_if_exist(self, code: int) -> Optional[ScheduleTravelStatusResponse]:
        ...

    async def get_current(self, code: int) -> Optional[ScheduleTravelResponse]:
        schedules = await self.schedule_service.get(code)

        if len(schedules) == 0:
            return None

        user = await self.user_service.get(code)

        schedule = schedules[0]

        return ScheduleTravelResponse(
            uuid=schedule.pk,
            driver=DriverUser(
                code=user.code,
                firstName=user.first_name,
                maternalSurname=user.maternal_surname,
                paternalSurname=user.paternal_surname,
                position=GeoPoint(
                    longitude=0,
                    latitude=0,
                )
            ),
            price=schedule.price,
            terminate=False,
            cancel=False,
            starting=schedule.starting,
            terminated=None,
            seats=schedule.seats,
            origin=schedule.origin,
            destination=schedule.destination,
            genders=schedule.genders,
            waypoints=set()
        )

    async def get_all(self, limit=10) -> list[ScheduleTravelResponse]:
        ...

    async def search(self, code: int, role: RoleUser, options: FilteringOptionsRequest, limit: int):
        return []

    async def update(self, code: int, role: RoleUser, req: ScheduleTravelUpdateRequest):
        ...


@functools.lru_cache
def get_schedule_use_case():
    return ScheduleTravelUseCase()
