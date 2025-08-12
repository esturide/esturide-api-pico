import contextlib
import functools

from app.core.exception import NotFoundException, InvalidRequestException
from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.user import User
from app.shared.scheme import StatusFailure, StatusSuccess
from app.shared.scheme.respose.schedule import create_schedule_response
from app.shared.scheme.rides import RideTravelUpdateRequest
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types import UUID
from app.shared.types.enum import RoleUser


class RideUseCase:
    def __init__(self):
        self.ride_service = get_ride_service()
        self.schedule_service = get_schedule_service()
        self.user_service = get_user_service()

    @contextlib.asynccontextmanager
    async def delete_ride(self, passenger: User, schedule: ScheduleTravel, ride: RideTravel):
        if ride.seat in schedule.seats:
            raise InvalidRequestException(
                "The seat was not found."
            )

        if not schedule.is_active:
            schedule.seats.append(ride.seat)

        if not schedule.is_active and schedule.passengers is not None and ride in schedule.passengers:
            schedule.passengers.remove(ride)

        yield ride

        await self.schedule_service.save(schedule)
        await self.ride_service.save(ride)

    async def create(self, code: int, role: RoleUser, schedule: ScheduleTravel, seat: str):
        passenger = await self.user_service.get(code)

        all_rides = await self.ride_service.get_all_rides_from_user(passenger)

        if len(all_rides) > 0 and not all([ride.is_finished for ride in all_rides]):
            return StatusFailure(
                message="You have a pending ride."
            )

        ride = await self.ride_service.create(passenger, seat)

        if seat in schedule.seats:
            schedule.seats.remove(seat)
        else:
            raise InvalidRequestException(
                "The seat has already been reserved."
            )

        if schedule.passengers is None:
            schedule.passengers = []

        schedule.passengers.append(ride)

        await self.schedule_service.save(schedule)

        return StatusSuccess(
            message="Ride created successfully."
        )

    async def get_current_from_user(self, user: User) -> tuple[ScheduleTravel, RideTravel]:
        all_rides = await self.ride_service.get_all_rides_from_user(user)
        if len(all_rides) == 0 or all([ride.is_finished for ride in all_rides]):
            raise NotFoundException("You don't have any pending ride.")

        ride = all_rides[0]

        schedule = await self.schedule_service.get_from_ride(ride)

        if ride is None:
            raise NotFoundException("Ride not found.")

        return schedule, ride

    async def current(self, code: int, role: RoleUser) -> RideTravelStatusResponse:
        if not role == RoleUser.passenger:
            raise InvalidRequestException()

        passenger = await self.user_service.get(code)
        schedule, ride = await self.get_current_from_user(passenger)

        return RideTravelStatusResponse(
            uuid=ride.id,
            seat=ride.seat,
            cancel=ride.cancel,
            over=ride.over,
            accept=ride.accept,
            travel=create_schedule_response(schedule)
        )

    async def cancel(self, passenger: User, role: RoleUser, schedule: ScheduleTravel, ride: RideTravel):
        async with self.delete_ride(passenger, schedule, ride) as ride:
            ride.cancel = True

        return StatusSuccess(
            message="Ride cancel."
        )

    async def over(self, passenger: User, role: RoleUser, schedule: ScheduleTravel, ride: RideTravel):
        async with self.delete_ride(passenger, schedule, ride) as ride:
            ride.over = True

        return StatusSuccess(
            message="Ride over."
        )

    async def update(self, req: RideTravelUpdateRequest, code: int, role: RoleUser):
        passenger = await self.user_service.get(code)
        schedule, ride = await self.get_current_from_user(passenger)

        if req.cancel:
            return await self.cancel(passenger, role, schedule, ride)
        elif req.over:
            return await self.over(passenger, role, schedule, ride)

        return StatusSuccess(
            message="No changes were made to the ride."
        )

    async def notify(self, code: int, role: RoleUser, schedule_id: UUID):
        pass


@functools.lru_cache
def get_ride_use_case():
    return RideUseCase()
