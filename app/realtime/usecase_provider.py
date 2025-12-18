from app.application.usecase.tracking import get_tracking_use_case, TrackingUseCase
from app.application.usecase.ride import get_ride_use_case, RideUseCase


def get_tracking_uc() -> TrackingUseCase:
    return get_tracking_use_case()


def get_ride_uc() -> RideUseCase:
    return get_ride_use_case()
