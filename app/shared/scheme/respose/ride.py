from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.scheme.respose.schedule import create_schedule_response
from app.shared.scheme.rides.status import RideTravelStatusResponse


def create_ride_response(schedule: ScheduleTravel, ride: RideTravel) -> RideTravelStatusResponse:
    return RideTravelStatusResponse(
        uuid=ride.id,
        seat=ride.seat,
        cancel=ride.cancel,
        over=ride.over,
        accept=ride.accept,
        travel=create_schedule_response(schedule)
    )
