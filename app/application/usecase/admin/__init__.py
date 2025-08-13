import functools

from app.core.exception import ResourceNotFoundException
from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusFailure, StatusSuccess, StatusMessage
from app.shared.scheme.admin.schedule import ChangesScheduleRequest


class AdminManagerUseCase:
    def __init__(self):
        self.user_service = get_user_service()
        self.schedule_service = get_schedule_service()
        self.ride_service = get_ride_service()

    async def change_schedule(self, code: int, req: ChangesScheduleRequest) -> StatusMessage:
        user = await self.user_service.get(code)

        if not user:
            raise ResourceNotFoundException("User not found.")

        if not user.is_admin:
            return StatusFailure()

        return StatusSuccess()


@functools.lru_cache
def get_admin_manager_use_case():
    return AdminManagerUseCase()
