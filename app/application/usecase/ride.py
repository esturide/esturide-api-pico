import contextlib
import functools

from app.core.exception import NotFoundException, InvalidRequestException
from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.scheme import StatusFailure, StatusSuccess
from app.shared.scheme.respose.schedule import create_schedule_response
from app.shared.scheme.rides import RideTravelResponse
from app.shared.types import UUID
from app.shared.types.enum import RoleUser


class RideUseCase:
    def __init__(self):
        self.ride_service = get_ride_service()
        self.schedule_service = get_schedule_service()
        self.user_service = get_user_service()

    @contextlib.asynccontextmanager
    async def delete_ride(self, code: int, schedule_id: UUID, remove_seat=False, remove_passenger=False):
        schedule = await self.schedule_service.get(schedule_id)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        passenger = await self.user_service.get(code)

        all_rides = await self.ride_service.get_all_rides_from_user(passenger)

        all_rides = list(filter(lambda r: r.is_current, all_rides))

        if not len(all_rides) >= 1:
            raise NotFoundException("You don't have any pending rides.")

        ride = all_rides[0]

        if ride.seat in schedule.seats:
            raise InvalidRequestException(
                "The seat was not found."
            )

        if remove_seat:
            schedule.seats.append(ride.seat)

        if remove_passenger and schedule.passengers is not None:
            schedule.passengers.remove(ride)

        yield ride

        await self.schedule_service.save(schedule)
        await self.ride_service.save(ride)

    async def create(self, code: int, role: RoleUser, schedule_id: UUID, seat: str):
        schedule = await self.schedule_service.get(schedule_id)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

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

    async def current(self, code: int, role: RoleUser) -> RideTravelResponse:
        user = await self.user_service.get(code)

        if user is None:
            raise NotFoundException("User not found.")

        all_ride = await self.ride_service.get_all_rides_from_user(user)
        ride = all_ride[0]

        schedule = await self.schedule_service.get_from_ride(ride)

        if ride is None:
            raise NotFoundException("Ride not found.")

        return RideTravelResponse(
            uuid=ride.id,
            seat=ride.seat,
            cancel=ride.cancel,
            over=ride.over,
            accept=ride.accept,
            travel=create_schedule_response(schedule)
        )

    async def cancel(self, code: int, role: RoleUser, schedule_id: UUID):
        async with self.delete_ride(code, schedule_id) as ride:
            ride.cancel = True

        return StatusSuccess(
            message="Ride cancel."
        )

    async def over(self, code: int, role: RoleUser, schedule_id: UUID):
        async with self.delete_ride(code, schedule_id) as ride:
            ride.over = True

        return StatusSuccess(
            message="Ride over."
        )

    async def notify(self, code: int, role: RoleUser, schedule_id: UUID):
        pass


@functools.lru_cache
def get_ride_use_case():
    return RideUseCase()
