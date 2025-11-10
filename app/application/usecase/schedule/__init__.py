import asyncio
import functools
from typing import Optional

from fastapi import BackgroundTasks
from geopy.geocoders.base import Geocoder

from app.core.exception import InvalidRequestException, NotFoundException
from app.domain.service.auth import AuthenticationCredentialsService
from app.domain.service.location.route import RouteService
from app.domain.service.location.search import SearchService
from app.domain.service.schedule import get_schedule_service, ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.const import DEFAULT_MAX_SCHEDULE_LIFETIME_SEC
from app.shared.dependencies.depends import GoogleMapsClient
from app.shared.models.travel import ScheduleTravelModel
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.respose.schedule import model_schedule_response, schedule_status_response
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import RoleUser


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = get_schedule_service()
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

        origin_result = await search_service.search(req.origin)
        destination_result = await search_service.search(req.destination)

        origin_address, origin_position = origin_result[0]
        destination_address, destination_position = destination_result[0]

        route_results = await route_service.routing(origin_address, destination_address, req.waypoints, req.starting)
        route_steps = route_results[0][1]

        schedule = await self.schedule_service.create(
            user=user,
            origin=origin_address,
            destination=destination_address,
            starting=req.starting,
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

    async def find_schedule_if_exist(self, code: int) -> Optional[ScheduleTravelStatusResponse]:
        user = await self.user_service.get(code)
        schedule = await self.schedule_service.get_current(user=user)

        if schedule is None:
            return None

        if schedule.is_finished:
            return None

        if schedule.lifetime_exceeded:
            return None

        return schedule_status_response(schedule)

    async def get_current(self, code: int) -> ScheduleTravelStatusResponse:
        user = await self.user_service.get(code)
        schedule = await self.schedule_service.get_current(user=user)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        if schedule.is_finished:
            raise NotFoundException("You currently have no scheduled trips available.")

        if schedule.lifetime_exceeded:
            raise NotFoundException("The life limit has been exceeded.")

        return schedule_status_response(schedule)

    async def get_all(self, limit=10) -> list[ScheduleTravelResponse]:
        async def iter_all_schedules():
            for schedule in await self.schedule_service.all(limit):
                yield model_schedule_response(schedule)

        return [schedule async for schedule in iter_all_schedules()]

    async def search(self, code: int, role: RoleUser, options: FilteringOptionsRequest, limit: int):
        async def iter_all_schedules_and_filtering():
            for schedule in await self.schedule_service.filtering(options, limit):
                yield model_schedule_response(schedule)

        return [schedule async for schedule in iter_all_schedules_and_filtering()]

    async def update(self, code: int, role: RoleUser, req: ScheduleTravelUpdateRequest):
        user = await self.user_service.get(code)

        if not user.is_valid_driver:
            raise InvalidRequestException("You cannot make the following changes.")

        schedule = await self.schedule_service.get_current(user=user)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        if schedule.is_finished:
            raise InvalidRequestException("You cannot make the following changes.")

        if req.starting is not None:
            schedule.starting = req.starting

        if any((req.cancel, req.terminate)):
            status, schedule = await self.schedule_service.finished(schedule, req.cancel, req.terminate)

        status = await self.schedule_service.save(schedule)

        if status:
            return StatusSuccess(
                message="Changes applied to the scheduled trip."
            )

        return StatusFailure(
            message="Changes not applied to the scheduled trip."
        )


@functools.lru_cache
def get_schedule_use_case():
    return ScheduleTravelUseCase()
