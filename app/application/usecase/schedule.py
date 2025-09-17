import asyncio
import functools

from fastapi import BackgroundTasks
from geopy.geocoders.base import Geocoder

from app.core.exception import InvalidRequestException, NotFoundException
from app.domain.service.auth import get_auth_service
from app.domain.service.schedule import get_schedule_service, ScheduleTravelService
from app.domain.service.user import get_user_service
from app.shared.const import DEFAULT_MAX_SCHEDULE_LIFETIME_SEC
from app.shared.models.schedule import ScheduleTravel
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.respose.schedule import create_schedule_response, create_schedule_status_response
from app.shared.scheme.schedule import ScheduleTravelResponse, ScheduleTravelUpdateRequest, \
    ScheduleTravelFromAddressRequest
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import RoleUser


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = get_schedule_service()
        self.user_service = get_user_service()
        self.auth_service = get_auth_service()

    async def create(self, req: ScheduleTravelFromAddressRequest, code: int, role: RoleUser, geocoder: Geocoder,
                     background_tasks: BackgroundTasks):
        def create_task(schedule_service: ScheduleTravelService, schedule: ScheduleTravel):
            async def task():
                await asyncio.sleep(DEFAULT_MAX_SCHEDULE_LIFETIME_SEC)

                schedule.cancel = True

                await schedule_service.save(schedule)

            return task

        if role != RoleUser.driver:
            raise InvalidRequestException('Role must be driver.')

        user = await self.user_service.get(code)

        if not user.is_valid_driver:
            raise InvalidRequestException('User is not an approved driver.')

        all_schedule = await self.schedule_service.get_by_driver(user)

        if len(all_schedule) != 0 and all([not schedule.is_finished for schedule in all_schedule]):
            raise InvalidRequestException("You currently have a pending trip.")

        schedule = await self.schedule_service.create(geocoder, req, user)

        if schedule is None:
            return StatusFailure(
                message="The trip could not be scheduled."
            )

        background_tasks.add_task(create_task(self.schedule_service, schedule))

        return StatusSuccess(
            message="New schedule traveled successfully."
        )

    async def get_current(self, code: int) -> ScheduleTravelStatusResponse:
        user = await self.user_service.get(code)
        schedule = await self.schedule_service.get_current(user=user)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        if schedule.is_finished:
            raise NotFoundException("You currently have no scheduled trips available.")

        if schedule.lifetime_exceeded:
            schedule.cancel = True
            await self.schedule_service.save(schedule)

            raise InvalidRequestException("Currently the trip has exceeded the life time limit.")

        return create_schedule_status_response(schedule)

    async def get_all(self, limit=10) -> list[ScheduleTravelResponse]:
        async def iter_all_schedules():
            for schedule in await self.schedule_service.all(limit):
                yield create_schedule_response(schedule)

        return [schedule async for schedule in iter_all_schedules()]

    async def search(self, code: int, role: RoleUser, options: FilteringOptionsRequest, limit: int):
        async def iter_all_schedules_and_filtering():
            for schedule in await self.schedule_service.filtering(options, limit):
                yield create_schedule_response(schedule)

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
