from fireo.fields import TextField, IDField, DateTime, NumberField
from fireo.models import Model

from app.shared.encrypt import check_same_password
from app.shared.fields import UserRoleField
from app.shared.types.enum import RoleUser


class User(Model):
    class Meta:
        collection_name = "users"

    id = IDField()
    created = DateTime(auto=True)

    hashed_password = TextField(required=True)
    salt = TextField(required=True)

    code = NumberField(required=True)

    first_name = TextField(required=True)
    paternal_surname = TextField()
    maternal_surname = TextField()
    birth_date = DateTime(required=True)
    email = TextField(required=True)
    curp = TextField(required=True)
    phone_number = TextField()
    address = TextField()

    role = UserRoleField(default=RoleUser.not_verified)

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
