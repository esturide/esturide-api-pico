import datetime

from redis_om import HashModel, Field

from app.shared.dependencies.depends.db import get_cache


class RegisterCustomer(HashModel):
    id: str = Field(index=True)
    created: datetime.datetime = Field(index=True, default=lambda: datetime.utcnow())


    class Meta:
        model_key_prefix = "register_customer"
