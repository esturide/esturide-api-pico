from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.pattern.singleton import Singleton


class TravelService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_store_repository = ScheduleStoreRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    def create(self):
        pass

