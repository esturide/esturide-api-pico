import datetime
import uuid

from app.infrestructure.repository.client.db import ClientDocumentRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.utils import async_task


class RideRepository(ClientDocumentRepository, metaclass=Singleton):
    async def get(self, uuid: uuid.UUID) -> RideTravelModel | None:
        def get_ride():
            return RideTravelModel.collection.get_from_user(id=uuid)

        return await async_task(get_ride)

    async def filter(
            self,
            passenger: UserDocument,
            over=False,
            order_date=True,
            seat: str | None = None,
            between: tuple[datetime.datetime, datetime.datetime] | None = None,
            limit: int = 10
    ) -> list[RideTravelModel]:
        def filter_rides():
            rides = RideTravelModel.collection.filter(passenger=passenger)

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
