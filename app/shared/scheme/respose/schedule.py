from app.shared.models.schedule import ScheduleTravel
from app.shared.scheme.location import GeoLocationModel, GeoLocationAddressModel
from app.shared.scheme.rides.status import RidePassengerResponse
from app.shared.scheme.schedule import ScheduleTravelResponse, DriverUser, PassengerUser
from app.shared.scheme.schedule.status import ScheduleTravelStatusResponse
from app.shared.types.enum import Gender


def create_schedule_response(schedule: ScheduleTravel) -> ScheduleTravelResponse:
    driver = schedule.driver
    all_passengers = schedule.rides

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

    origin = GeoLocationAddressModel(
        longitude=schedule.origin.location.longitude,
        latitude=schedule.origin.location.latitude,
        address=schedule.origin.address,
    )

    destination = GeoLocationAddressModel(
        longitude=schedule.destination.location.longitude,
        latitude=schedule.destination.location.latitude,
        address=schedule.destination.address,
    )

    return ScheduleTravelResponse(
        uuid=schedule.id,
        driver=driver_response,
        price=schedule.price,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        starting=schedule.starting,
        terminated=schedule.terminated,
        maxPassengers=schedule.max_passengers,
        seats=schedule.seats,
        origin=origin,
        destination=destination,
        genderFilter=schedule.accepted_genres
    )


def create_schedule_status_response(schedule: ScheduleTravel) -> ScheduleTravelStatusResponse:
    driver = schedule.driver
    all_passengers = schedule.rides

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

    all_rides = []

    if all_passengers is not None:
        for ride in all_passengers:
            passenger = ride.passenger

            passenger_user_model = PassengerUser(
                code=passenger.code,
                firstName=passenger.first_name,
                maternalSurname=passenger.maternal_surname,
                paternalSurname=passenger.paternal_surname,
                position=GeoLocationModel(
                    latitude=0,
                    longitude=0,
                )
            )

            ride_response_model = RidePassengerResponse(
                uuid=ride.id,
                seat=ride.seat,
                cancel=ride.cancel,
                over=ride.over,
                accept=ride.accept,
                passenger=passenger_user_model,
            )

            all_rides.append(ride_response_model)

    origin = GeoLocationAddressModel(
        longitude=schedule.origin.location.longitude,
        latitude=schedule.origin.location.latitude,
        address=schedule.origin.address
    )

    destination = GeoLocationAddressModel(
        longitude=schedule.destination.location.longitude,
        latitude=schedule.destination.location.latitude,
        address=schedule.destination.address
    )

    return ScheduleTravelStatusResponse(
        uuid=schedule.id,
        driver=driver_response,
        price=schedule.price,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        starting=schedule.starting,
        terminated=schedule.terminated,
        maxPassengers=schedule.max_passengers,
        seats=schedule.seats,
        origin=origin,
        destination=destination,
        rides=all_rides,
        genderFilter=schedule.accepted_genres
    )
