from fireo.fields import TextField, IDField, DateTime, NumberField
from fireo.models import Model

from app.shared.encrypt import check_same_password
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

    role = TextField(default=RoleUser.not_verified.value)

    def same_password(self, password) -> bool:
        return check_same_password(
            password,
            self.hashed_password
        )
