import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, Field, model_validator

from app.shared.types import GenderOption


class FilteringOptionsRequest(BaseModel):
    order_by_date: bool = Field(default=False, title="Order by date", alias='orderByDate')

    origin: Optional[str] = Field(default=None, alias='origin')
    destination: Optional[str] = Field(default=None, alias='destination')

    terminate: bool = Field(default=False)
    cancel: bool = Field(default=False)

    range_date: Tuple[datetime.datetime, datetime.datetime] = Field(default=None, alias='rangeDate')
    price_range: Tuple[float, float] = Field(default=None, alias='priceRange')
    gender: GenderOption = Field({'male', 'female'}, alias='gender')

    @model_validator(mode='after')
    def validate_dates(self):
        if self.max_price is not None:
            if self.min_price >= self.max_price:
                raise ValueError('Invalid price.')

        if self.starting is not None and self.terminated is not None:
            if self.starting > self.terminated:
                raise ValueError('Valid dates, you cannot see a trip that starts after you have finished.')

        return self
