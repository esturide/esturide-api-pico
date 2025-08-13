import functools

from google.cloud.firestore import GeoPoint

from app.core.exception import ResourceNotFoundException, InvalidRequestException
from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.tracking import TrackingService
from app.domain.service.user import get_user_service
from app.shared.models.tracking import TrackingRecord
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.location import GeoLocationModel
from app.shared.types.enum import RoleUser, Status


class TrackingUseCase:
    def __init__(self):
        self.user_service = get_user_service()
        self.ride_service = get_ride_service()
        self.schedule_service = get_schedule_service()
        self.tracking_service = TrackingService()

    async def register(self, code: int, role: RoleUser, location: GeoLocationModel):
        status = False
        user = await self.user_service.get(code)

        tracking = TrackingRecord()
        tracking.location = GeoPoint(
            location.latitude,
            location.longitude,
        )


        if role == RoleUser.passenger:
            ride = await self.ride_service.get_current_ride_from_user(user)

            if ride is None:
                raise ResourceNotFoundException(detail="They don't have any active rides.")

            status = await self.tracking_service.register_ride(ride, tracking)
        elif role == RoleUser.driver:
            schedule = await self.schedule_service.get_current(user)

            if schedule is None:
                raise ResourceNotFoundException(detail="They don't have any active schedule.")

            status = await self.tracking_service.register_schedule(schedule, tracking)
        else:
            raise InvalidRequestException(detail="Invalid role request.")

        if status:
            return StatusSuccess(message="Record registered successfully.")

        return StatusFailure(message="Something went wrong.")


@functools.lru_cache
def get_tracking_use_case():
    return TrackingUseCase()
