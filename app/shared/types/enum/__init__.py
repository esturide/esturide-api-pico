import enum


class Status(enum.StrEnum):
    success = 'success'
    failure = 'failure'


class Gender(enum.StrEnum):
    male = 'male'
    female = 'female'
    other = 'other'


class StatusTravel(enum.StrEnum):
    start = 'start'
    terminate = 'terminate'
    cancel = 'cancel'


class TypeRole(enum.StrEnum):
    passenger = 'passenger'
    driver = 'driver'


class RoleUser(enum.StrEnum):
    not_verified = 'not-verified'
    standard = 'standard'
    passenger = 'passenger'
    driver = 'driver'
    staff = 'staff'
    admin = 'admin'


class CurrentSession(enum.StrEnum):
    travel = 'travel'
    ride = 'ride'
    free = 'free'
