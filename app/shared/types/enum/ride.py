import enum


class RideStatus(enum.StrEnum):
    waiting = "waiting"
    accepted = "accepted"
    rejected = "rejected"
