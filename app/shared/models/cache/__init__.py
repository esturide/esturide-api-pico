from redis_om import HashModel, Field

from app.shared.dependencies import get_async_cache


class PassengerRide(HashModel):
    id: str = Field(index=True)


    class Meta:
        database = get_async_cache()
