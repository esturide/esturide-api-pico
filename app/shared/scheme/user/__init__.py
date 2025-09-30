import datetime

from pydantic import BaseModel, Field, field_validator, SecretStr, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.shared.types.enum import RoleUser


class UserProfile(BaseModel):
    usercode: int

    firstname: str = Field(..., title="firstName", alias="firstName")
    maternal_surname: str = Field(..., title="maternalSurname", alias="maternalSurname")
    paternal_surname: str = Field(..., title="paternalSurname", alias="paternalSurname")
    curp: str = Field(..., title="CURP", alias='curp')
    birth_date: datetime.date = Field(..., title="Birth date", alias="birthDate", description="The user's birth date")
    phone_number: PhoneNumber = Field(..., title="Phone number", alias="phoneNumber")
    email: EmailStr = Field(..., title="Email", alias='email')
    address: str = Field(..., title="Address user", alias="address")

    @field_validator('birth_date')
    def check_age(cls, birth_date):
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValueError('The person must be over 18 years old.')

        return birth_date


class UserRequest(UserProfile):
    password: SecretStr


class UserResponse(BaseModel):
    code: int

    first_name: str = Field(..., title="firstName", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')

    email: EmailStr = Field(..., title="Email", alias='email')

    role: RoleUser = RoleUser.not_verified


class ProfileUpdateRequest(BaseModel):
    first_name: str
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    curp: str
    birth_date: datetime.date = Field(..., title="Birth date", alias='birthDate')

    email: EmailStr = Field(..., title="Email", alias='email')
    password: SecretStr


class AutomobileProfile(BaseModel):
    brand: str
    year: str
    model: int


class RoleUpdateRequest(BaseModel):
    role: RoleUser
