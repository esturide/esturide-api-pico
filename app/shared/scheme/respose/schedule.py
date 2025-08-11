from app.shared.models.schedule import ScheduleTravel
from app.shared.scheme.location import GeoLocationModel
from app.shared.scheme.schedule import ScheduleTravelResponse, DriverUser, PassengerUser
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse


def create_schedule_response(schedule: ScheduleTravel) -> ScheduleTravelResponse:
    driver = schedule.driver
    all_passengers = schedule.passengers

    driver_response = DriverUser(
        code=driver.code,
        firstName=driver.first_name,
        maternalSurname=driver.maternal_surname,
        paternalSurname=driver.paternal_surname,
        position=GeoLocationModel(
            latitude=0,
            longitude=0,
        )
    )

    """
    all_passengers_response = [
        PassengerUser(
            code=ride.passenger.code,
            firstName=ride.passenger.first_name,
            maternalSurname=ride.passenger.maternal_surname,
            paternalSurname=ride.passenger.paternal_surname,
            position=GeoLocationModel(
                latitude=0,
                longitude=0,
            )
        ) for ride in all_passengers
    ] if all_passengers is not None else []
    """

    origin = GeoLocationModel(
        longitude=schedule.origin.longitude,
        latitude=schedule.origin.latitude,
    )

    destination = GeoLocationModel(
        longitude=schedule.destination.longitude,
        latitude=schedule.destination.latitude,
    )

    return ScheduleTravelResponse(
        uuid=schedule.id,
        driver=driver_response,
        price=schedule.price,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        starting=schedule.starting,
        terminated=None,
        maxPassengers=schedule.max_passengers,
        seats=schedule.seats,
        origin=origin,
        destination=destination,
    )



def create_schedule_status_response(schedule: ScheduleTravel) -> ScheduleTravelStatusResponse:
    driver = schedule.driver
    all_passengers = schedule.passengers

    driver_response = DriverUser(
        code=driver.code,
        firstName=driver.first_name,
        maternalSurname=driver.maternal_surname,
        paternalSurname=driver.paternal_surname,
        position=GeoLocationModel(
            latitude=0,
            longitude=0,
        )
    )

    all_passengers_response = [
        PassengerUser(
            code=ride.passenger.code,
            firstName=ride.passenger.first_name,
            maternalSurname=ride.passenger.maternal_surname,
            paternalSurname=ride.passenger.paternal_surname,
            position=GeoLocationModel(
                latitude=0,
                longitude=0,
            )
        ) for ride in all_passengers
    ] if all_passengers is not None else []

    origin = GeoLocationModel(
        longitude=schedule.origin.longitude,
        latitude=schedule.origin.latitude,
    )

    destination = GeoLocationModel(
        longitude=schedule.destination.longitude,
        latitude=schedule.destination.latitude,
    )

    return ScheduleTravelResponse(
        uuid=schedule.id,
        driver=driver_response,
        price=schedule.price,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        starting=schedule.starting,
        terminated=None,
        maxPassengers=schedule.max_passengers,
        seats=schedule.seats,
        origin=origin,
        destination=destination,
    )
