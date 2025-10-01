import datetime

from app.infrestructure.repository.firebase import AsyncSessionRepository
from app.shared.models.ride import RideTravel
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.types import UUID
from app.shared.utils import async_task


class RideRepository(AsyncSessionRepository, metaclass=Singleton):
    async def get(self, uuid: UUID) -> RideTravel | None:
        def get_ride():
            return RideTravel.collection.get(id=uuid)

        return await async_task(get_ride)

    async def filter(
            self,
            passenger: User,
            over=False,
            order_date=True,
            seat: str | None = None,
            between: tuple[datetime.datetime, datetime.datetime] | None = None,
            limit: int = 10
    ) -> list[RideTravel]:
        def filter_rides():
            rides = RideTravel.collection.filter(passenger=passenger)

            if between is not None:
                before, after = between

                rides = (rides
                         .filter('starting', '>=', before)
                         .filter('starting', '<=', after))

            if seat is not None:
                rides = rides.filter(seat=seat)

            rides = rides.filter(over=over)

            if order_date:
                rides = rides.order('-created')

            return list(rides.fetch(limit))

        return await async_task(filter_rides)
