import datetime
import typing

from pydantic import BaseModel, Field, model_validator

from app.shared.scheme.location import GeoLocationModel


class FilteringOptionsRequest(BaseModel):
    origin: str
    destination: str

    terminate: bool = Field(False)
    cancel: bool = Field(False)

    starting: typing.Optional[datetime.datetime] = Field(None)
    terminated: typing.Optional[datetime.datetime] = Field(None)

    min_price: float = Field(1, ge=0)
    max_price: typing.Optional[float] = Field(None)

    origin: typing.Optional[GeoLocationModel] = Field(None)
    destination: typing.Optional[GeoLocationModel] = Field(None)

    order_by_date: bool = Field(False, title="Order by date", alias='orderByDate')

    seats: typing.Set[str] = Field(['A', 'B', 'C'], alias='seats')

    @model_validator(mode='after')
    def validate_dates(self) -> 'FilteringOptionsRequest':
        if self.max_price is not None:
            if self.min_price >= self.max_price:
                raise ValueError('Invalid price.')

        if self.starting is not None and self.terminated is not None:
            if self.starting > self.terminated:
                raise ValueError('Valid dates, you cannot see a trip that starts after you have finished.')

        return self
