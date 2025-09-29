import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator, field_validator

from app.shared.types import SeatList, GenderList


class FilteringOptionsRequest(BaseModel):
    origin: Optional[str] = Field(default=None, alias='origin')
    destination: Optional[str] = Field(default=None, alias='destination')

    terminate: bool = Field(False)
    cancel: bool = Field(False)

    starting: Optional[datetime.datetime] = Field(default=None, alias='starting', description='Start date and time')
    terminated: Optional[datetime.datetime] = Field(default=None, alias='terminated', description='End date and time')

    min_price: float = Field(1, ge=1, alias='minPrice')
    max_price: Optional[float] = Field(default=None, alias='maxPrice')

    order_by_date: bool = Field(default=None, title="Order by date", alias='orderByDate')

    seats: SeatList = Field({'A', 'B', 'C'}, alias='seats')

    gender: GenderList = Field({'male', 'female'}, alias='gender')

    @model_validator(mode='after')
    def validate_dates(self):
        if self.max_price is not None:
            if self.min_price >= self.max_price:
                raise ValueError('Invalid price.')

        if self.starting is not None and self.terminated is not None:
            if self.starting > self.terminated:
                raise ValueError('Valid dates, you cannot see a trip that starts after you have finished.')

        return self
