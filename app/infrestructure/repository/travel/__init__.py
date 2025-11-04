from typing import Optional

from app.core.exception import InvalidRequestException
from app.infrestructure.repository.client.db import ClientDocumentRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.travel import ScheduleTravelModel
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.types import SeatList, GenderList


class TravelRepository(ClientDocumentRepository, metaclass=Singleton):
    async def filtering(
            self,
            terminate=False,
            cancel=False,
            starting=None,
            terminated=None,
            price_range: tuple[float, float | None] = (1, None),
            order_date: bool = False,
            limit: int = 10,
            seats: Optional[SeatList] = None,
            genders: Optional[GenderList] = None,
    ) -> list[ScheduleTravelModel]:
        """
        if seats is None:
            seats = {Seats.A, Seats.C, Seats.B}

        if genders is None:
            genders = {Gender.male, Gender.female}
        def filter_schedule():
            min_price, max_price = price_range

            if max_price is not None and min_price >= max_price:
                raise InvalidRequestException('Price range must be greater than or equal to 1.')

            schedules = (ScheduleTravel.collection
                         .filter(terminate=terminate, cancel=cancel)
                         .filter('price', '>=', min_price))

            if starting is not None:
                schedules = schedules.filter('starting', '>=', starting)

            if terminated is not None:
                schedules = schedules.filter('terminated', '>=', terminated)

            if max_price is not None:
                schedules = schedules.filter('price', '<=', max_price)

            if order_date:
                schedules = schedules.order('-created')

            return list(schedules.fetch(limit))

        seats_filter = set([seat.value for seat in seats])
        genders_filter = set([gender.value for gender in genders])

        all_schedules = await async_task(filter_schedule)
        """

        return []

    async def get_from_code(self, code: int) -> ScheduleTravelModel:
        return await ScheduleTravelModel.find_one(ScheduleTravelModel.code == code)

    async def get_current(self, user: User | None = None, ride: RideTravelModel | None = None,
                          *args) -> ScheduleTravelModel | None:
        """
        def filter_schedule_task_driver():
            return list(ScheduleTravel.collection
                        .filter(driver=user)
                        .order('-created')
                        .fetch())

        def filter_schedule_task_passenger():
            return list(ScheduleTravel.collection
                        .filter('rides', 'array_contains', ride)
                        .fetch())

        all_schedule = []

        if user is not None:
            all_schedule = await async_task(filter_schedule_task_driver)
        elif ride is not None:
            all_schedule = await async_task(filter_schedule_task_passenger)
        else:
            raise InvalidRequestException("You cannot make the request with the current user role.")

        if len(all_schedule) == 0:
            return None
        """

        return None

    async def get_by_driver(self, user: User, limit=10) -> list[ScheduleTravelModel]:
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        return await (ScheduleTravelModel
                      .find(ScheduleTravelModel.driver == user)
                      .sort("-created")
                      .limit(limit)
                      .to_list())

    async def get_by_passenger(self, user: User, limit=10) -> list[ScheduleTravelModel]:
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        return await (ScheduleTravelModel
                      .find({'rides.passenger': user})
                      .sort("-created")
                      .to_list())

    async def get_all(self, limit=10):
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        return await (ScheduleTravelModel
                      .find()
                      .sort("-created")
                      .limit(limit)
                      .to_list())
