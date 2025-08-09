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


class RoleUser(str, enum.Enum):
    not_verified = 'not-verified'
    driver = 'driver'
    passenger = 'passenger'
    staff = 'staff'
    admin = 'admin'


class CurrentRuleUser(str, enum.Enum):
    no_session = 'no-session'
    driver = 'driver'
    passenger = 'passenger'
