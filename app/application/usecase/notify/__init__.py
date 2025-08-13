from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service


class NotifyUseCase:
    def __init__(self, app):
        self.ride_service = get_ride_service()
        self.schedule_service = get_schedule_service()

    async def notify_ride(self):
        pass

