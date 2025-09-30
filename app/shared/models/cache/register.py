import datetime

from redis_om import HashModel, Field


class RegisterCustomer(HashModel):
    id: str = Field(index=True)
    created: datetime.datetime = Field(index=True, default=lambda: datetime.utcnow())


    class Meta:
        model_key_prefix = "register_customer"
