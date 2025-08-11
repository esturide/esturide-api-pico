import functools

from app.core.exception import ValidationException, InvalidRequestException
from app.domain.service.auth import get_auth_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusSuccess
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.respose.schedule import create_schedule_response, create_schedule_status_response
from app.shared.scheme.schedule import ScheduleTravelRequest, ScheduleTravelResponse, ScheduleTravelUpdateRequest
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import RoleUser, Status


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = get_schedule_service()
        self.user_service = get_user_service()
        self.auth_service = get_auth_service()

    async def create(self, req: ScheduleTravelRequest, code: int):
        if not req.price >= 1:
            raise ValidationException("Invalid price.")

        user = await self.user_service.get(code)

        if not user.is_valid_driver:
            return False

        all_schedule = await self.schedule_service.get_by_driver(user)

        if len(all_schedule) != 0 and all([not schedule.is_finished for schedule in all_schedule]):
            raise InvalidRequestException("You currently have a pending trip.")

        await self.schedule_service.create(req, user)

        return StatusSuccess(
            message="New schedule traveled successfully."
        )

    async def get_current(self, code: int) -> ScheduleTravelStatusResponse:
        user = await self.user_service.get(code)
        schedule = await self.schedule_service.get_current(user=user)

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

        schedule.terminate = req.terminate if req.terminate else schedule.terminate
        schedule.cancel = req.cancel if req.cancel else schedule.cancel
        schedule.starting = req.starting if schedule.starting is None else schedule.starting
        schedule.terminated = req.terminated if schedule.terminated is None else schedule.terminated

        status = await self.schedule_service.save(schedule)

        if status:
            return {
                "status": Status.success,
                "message": "Schedule is updated.",
            }

        return {
            "status": Status.failure,
            "message": "Cannot updated schedule.",
        }


@functools.lru_cache
def get_schedule_use_case():
    return ScheduleTravelUseCase()
