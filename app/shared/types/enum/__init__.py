import enum


class Status(str, enum.Enum):
    success = 'success'
    failure = 'failure'


class Gender(str, enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class StatusTravel(str, enum.Enum):
    start = 'start'
    terminate = 'terminate'
    cancel = 'cancel'


class CurrentRuleUser(str, enum.Enum):
    no_session = 'no-session'
    driver = 'driver'
    passenger = 'passenger'


class RoleUser(enum.Enum):
    not_verified = 'not-verified'
    passenger = 'passenger'
    driver = 'driver'
    staff = 'staff'
    admin = 'admin'
