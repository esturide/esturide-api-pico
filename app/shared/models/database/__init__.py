import datetime

from sqlalchemy import Integer, Date, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.models.database.sql_base import Base
from app.shared.types.enum import RoleUser


class UserCustomer(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    usercode: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    created: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    salt: Mapped[str] = mapped_column(String(16), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(16), nullable=False)

    firstname: Mapped[str] = mapped_column(Text, nullable=False)
    paternal_surname: Mapped[str] = mapped_column(Text, nullable=False)
    maternal_surname: Mapped[str] = mapped_column(Text, nullable=False)
    birth_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    email: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    curp: Mapped[str] = mapped_column(Text, unique=True, index=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    phone_number: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    role_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    @property
    def role(self) -> RoleUser:
        roles = [
            RoleUser.not_verified,
            RoleUser.passenger,
            RoleUser.driver,
            RoleUser.staff,
            RoleUser.admin,
        ]

        return roles[self.role_level]
