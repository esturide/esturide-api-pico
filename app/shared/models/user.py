import datetime

from beanie import Document, Indexed
from pydantic import Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.shared.encrypt import check_same_password
from app.shared.types import Gender
from app.shared.types.enum import RoleUser


class UserDocument(Document):
    class Settings:
        collection = "Users"

    created: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    hashed_password: str
    salt: str

    code: int = Indexed(int, unique=True)

    first_name: str
    paternal_surname: str
    maternal_surname: str
    birth_date: datetime.datetime
    gender: Gender = Field(..., title="Gender")

    email: EmailStr = Field(..., title="Email")
    curp: str = Field(...)
    phone_number: PhoneNumber = Field(..., title="Phone number", )
    address: str = Field(...)

    role: RoleUser = Field(default=RoleUser.not_verified)

    def same_password(self, password) -> bool:
        return check_same_password(
            password,
            self.hashed_password
        )

    @property
    def is_verified(self):
        return RoleUser(self.role) != RoleUser.not_verified

    @property
    def is_valid_driver(self) -> bool:
        if RoleUser(self.role) in [RoleUser.driver, RoleUser.staff, RoleUser.admin]:
            return True

        return False

    @property
    def is_valid_passenger(self):
        role = RoleUser(self.role)

        return role != RoleUser.not_verified or role == RoleUser.passenger

    @property
    def is_valid_admin(self):
        return RoleUser(self.role) == RoleUser.admin

    @property
    def is_valid_staff(self):
        return RoleUser(self.role) == RoleUser.staff

    @property
    def usercode(self):
        return str(self.code)
