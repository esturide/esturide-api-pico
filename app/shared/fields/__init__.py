from fireo.fields import TextField

from app.shared.types.enum import RoleUser


class UserRoleField(TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_roles = [role.value for role in RoleUser]

    def db_value(self, value):
        if value is None:
            return None

        if isinstance(value, RoleUser):
            value = value.value

        if value not in self.valid_roles:
            raise ValueError(f"Rol '{value}' no válido. Válidos: {self.valid_roles}")

        return value

    def python_value(self, value):
        if value is None:
            return None

        return RoleUser(value)
