import functools

from app.core.exception import ValidationException, InvalidRequestException
from app.domain.service.auth import get_auth_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.models.schedule import ScheduleTravel
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.location import GeoLocationModel
from app.shared.scheme.schedule import ScheduleTravelRequest, ScheduleTravelResponse, DriverUser, PassengerUser, \
    ScheduleTravelUpdateRequest
from app.shared.types.enum import RoleUser, Status


class ScheduleTravelUseCase:
    def __init__(self):
        self.schedule_service = get_schedule_service()
        self.user_service = get_user_service()
        self.auth_service = get_auth_service()

    @staticmethod
    def create_schedule_response(schedule: ScheduleTravel) -> ScheduleTravelResponse:
        driver = schedule.driver
        all_passengers = schedule.passengers

        driver_response = DriverUser(
            code=driver.code,
            firstName=driver.first_name,
            maternalSurname=driver.maternal_surname,
            paternalSurname=driver.paternal_surname,
            position=GeoLocationModel(
                latitude=0,
                longitude=0,
            )
        )

        all_passengers_response = [
            PassengerUser(
                code=passenger.code,
                firstName=passenger.first_name,
                maternalSurname=passenger.maternal_surname,
                paternalSurname=passenger.paternal_surname,
                position=GeoLocationModel(
                    latitude=0,
                    longitude=0,
                )
            ) for passenger in all_passengers
        ] if all_passengers is not None else []

        origin = GeoLocationModel(
            longitude=schedule.origin.longitude,
            latitude=schedule.origin.latitude,
        )

        destination = GeoLocationModel(
            longitude=schedule.destination.longitude,
            latitude=schedule.destination.latitude,
        )

        return ScheduleTravelResponse(
            driver=driver_response,
            price=schedule.price,
            terminate=schedule.terminate,
            cancel=schedule.cancel,
            starting=schedule.starting,
            terminated=None,
            maxPassengers=schedule.max_passengers,
            seats=schedule.seats,
            passengers=all_passengers_response,
            origin=origin,
            destination=destination,
        )

    async def create(self, req: ScheduleTravelRequest, code: int):
        if not req.price >= 1:
            raise ValidationException("Invalid price.")

        user = await self.user_service.get(code)

        if not user.is_valid_driver:
            return False

        all_schedule = await self.schedule_service.get_by_driver(user)

        if len(all_schedule) != 0 and all([not schedule.is_finished for schedule in all_schedule]):
            raise InvalidRequestException("You currently have a pending trip.")

        status = await self.schedule_service.create(req, user)

        if status:
            return {
                "status": Status.success,
                "message": "New schedule traveled successfully.",
            }

        return {
            "status": Status.failure,
            "message": "Cannot schedule new travel.",
        }

    async def get_current(self, code: int) -> ScheduleTravelResponse:
        user = await self.user_service.get(code)
        schedule = await self.schedule_service.get_current(user, RoleUser.driver)

        return self.create_schedule_response(schedule)

    async def get_all(self, limit=10) -> list[ScheduleTravelResponse]:
        async def iter_all_schedules():
            for schedule in await self.schedule_service.all(limit):
                yield self.create_schedule_response(schedule)

        return [schedule async for schedule in iter_all_schedules()]

    async def search(self, code: int, role: RoleUser, options: FilteringOptionsRequest, limit: int):
        async def iter_all_schedules_and_filtering():
            for schedule in await self.schedule_service.filtering(options, limit):
                yield self.create_schedule_response(schedule)

        return [schedule async for schedule in iter_all_schedules_and_filtering()]

    async def update(self, code: int, role: RoleUser, req: ScheduleTravelUpdateRequest):
        user = await self.user_service.get(code)

        if not user.is_valid_driver:
            raise InvalidRequestException("You cannot make the following changes.")

        schedule = await self.schedule_service.get_current(user, role)

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
