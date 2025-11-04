from app.shared.models.ride import RideTravelModel
from app.shared.models.travel import ScheduleTravelModel
from app.shared.scheme.respose.schedule import model_schedule_response
from app.shared.scheme.rides.status import RideTravelStatusResponse


def create_ride_response(schedule: ScheduleTravelModel, ride: RideTravelModel) -> RideTravelStatusResponse:
    return RideTravelStatusResponse(
        uuid=ride.id,
        seat=ride.seat,
        cancel=ride.cancel,
        over=ride.over,
        accept=ride.accept,
        travel=model_schedule_response(schedule)
    )
