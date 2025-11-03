import functools

from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.schedule import ScheduleRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.schedule import ScheduleTravelModel
from app.shared.models.tracking import Tracking
from app.shared.pattern.singleton import Singleton


class TrackingService(metaclass=Singleton):
    def __init__(self):
        self.ride_depository = RideRepository()
        self.schedule_repository = ScheduleRepository()

    async def register_schedule(self, schedule: ScheduleTravelModel, tracking: Tracking):
        schedule.tracking.append(tracking)

        return await self.ride_depository.save(tracking) and await self.schedule_repository.save(schedule)

    async def register_ride(self, ride: RideTravelModel, tracking: Tracking):
        ride.tracking.append(tracking)

        return await self.ride_depository.save(tracking) and await self.schedule_repository.save(ride)


@functools.lru_cache
def get_tracking_service() -> TrackingService:
    return TrackingService()
