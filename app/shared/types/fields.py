from fireo.fields import Field

from app.shared.types.enum import RoleUser


class RoleField(Field):
    roles = [status.value for status in RoleUser]

    def db_value(self, val):
        return self.roles[val]

    def field_value(self, val):
        return self.roles.index(val)
