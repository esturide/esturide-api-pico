import asyncio
import contextlib
import functools
from typing import Optional

from fastapi import BackgroundTasks

from app.core.exception import NotFoundException, InvalidRequestException, ResourceNotFoundException
from app.domain.service.ride import RideService
from app.domain.service.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.const import DEFAULT_MAX_RIDE_LIFETIME_SEC
from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme import StatusFailure, StatusSuccess
from app.shared.scheme.respose.ride import create_ride_response
from app.shared.scheme.rides import RideTravelUpdateRequest, RideTravelRequest
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types import UUID
from app.shared.types.enum import RoleUser


class RideUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleTravelService()
        self.user_service = UserService()

    @contextlib.asynccontextmanager
    async def delete_ride(self, passenger: User, schedule: ScheduleTravel, ride: RideTravel):
        if ride.seat in schedule.seats:
            raise InvalidRequestException(
                "The seat was not found."
            )

        if not schedule.is_active:
            schedule.seats.append(ride.seat)

        if not schedule.is_active and schedule.rides is not None and ride in schedule.rides:
            schedule.rides.remove(ride)

        yield ride

        await self.schedule_service.save(schedule)
        await self.ride_service.save(ride)

    async def create(self, code: int, role: RoleUser, req: RideTravelRequest, background_tasks: BackgroundTasks):
        def create_task(ride_service: RideService, ride: RideTravel):
            async def task():
                await asyncio.sleep(DEFAULT_MAX_RIDE_LIFETIME_SEC)

                ride.cancel = True

                await ride_service.save(ride)

            return task

        passenger = await self.user_service.get(code)

        all_rides = await self.ride_service.get_all_rides_from_user(passenger)

        if len(all_rides) > 0 and not all([ride.is_finished for ride in all_rides]):
            return StatusFailure(
                message="You have a pending ride."
            )

        schedule = await self.schedule_service.get(req.uuid)
        ride = await self.ride_service.create(passenger, req.seat)

        if req.seat in schedule.seats:
            schedule.seats.remove(req.seat)
        else:
            raise InvalidRequestException(
                "The seat has already been reserved."
            )

        if schedule.rides is None:
            schedule.rides = []

        schedule.rides.append(ride)

        status = await self.schedule_service.save(schedule)

        if not status:
            return StatusFailure(
                message="The ride could not be booked."
            )

        background_tasks.add_task(create_task(self.ride_service, ride))

        return StatusSuccess(
            message="Ride created successfully."
        )

    async def get_current_from_user(self, user: User) -> tuple[ScheduleTravel | None, RideTravel | None]:
        all_rides = await self.ride_service.get_all_rides_from_user(user)

        if len(all_rides) == 0 or all([ride.is_finished for ride in all_rides]):
            return None, None

        ride = all_rides[0]

        schedule = await self.schedule_service.get_from_ride(ride)

        return schedule, ride

    async def find_ride_if_exist(self, code: int) -> Optional[RideTravelStatusResponse]:
        passenger = await self.user_service.get(code)
        schedule, ride = await self.get_current_from_user(passenger)

        if schedule is None and ride is None:
            return None

        if schedule.is_finished:
            return None

        if schedule is None:
            return None

        if ride is None:
            return None

        return create_ride_response(schedule, ride)

    async def current(self, code: int) -> RideTravelStatusResponse:
        passenger = await self.user_service.get(code)
        schedule, ride = await self.get_current_from_user(passenger)

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        if ride is None:
            raise NotFoundException("Ride not found.")

        if schedule.is_finished:
            raise ResourceNotFoundException("The scheduled trip has been cancelled.")

        return create_ride_response(schedule, ride)

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

        if schedule is None:
            raise NotFoundException("Schedule not found.")

        if ride is None:
            raise NotFoundException("Ride not found.")

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
