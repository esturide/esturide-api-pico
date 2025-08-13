import functools

from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.schedule import ScheduleRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.tracking import TrackingRecord


class TrackingService:
    async def register_schedule(self, schedule: ScheduleTravel, tracking: TrackingRecord):
        schedule.tracking.append(tracking)

        return await TrackingRepository.save(tracking) and await ScheduleRepository.save(schedule)

    async def register_ride(self, ride: RideTravel, tracking: TrackingRecord):
        ride.tracking.append(tracking)

        return await TrackingRepository.save(tracking) and await RideRepository.save(ride)


@functools.lru_cache
def get_tracking_service() -> TrackingService:
    return TrackingService()
