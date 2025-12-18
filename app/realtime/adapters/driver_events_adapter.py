from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.realtime.usecase_provider import get_tracking_uc, get_ride_uc


@dataclass(frozen=True)
class LocationUpdate:
    driver_id: int
    lat: float
    lng: float
    timestamp: datetime
    accuracy: float | None


@dataclass(frozen=True)
class TripStatusUpdate:
    driver_id: int
    trip_id: str
    status: str
    timestamp: datetime


class DriverEventsAdapter:
    """
    Conecta Socket.IO -> UseCases.
    Si las firmas reales no coinciden, ajustar SOLO en este archivo.
    """

    def __init__(self):
        self.tracking_uc = get_tracking_uc()
        self.ride_uc = get_ride_uc()

    async def handle_location_update(self, dto: LocationUpdate) -> dict:
        """
        Ajustar TrackingUseCase real.
        """
        if hasattr(self.tracking_uc, "update_driver_location"):
            await self.tracking_uc.update_driver_location(
                dto.driver_id,
                dto.lat,
                dto.lng,
                dto.timestamp,
                dto.accuracy,
            )
        elif hasattr(self.tracking_uc, "save_location"):
            await self.tracking_uc.save_location(
                driver_id=dto.driver_id,
                lat=dto.lat,
                lng=dto.lng,
                timestamp=dto.timestamp,
                accuracy=dto.accuracy,
            )
        else:
            raise AttributeError(
                "TrackingUseCase no expone update_driver_location ni save_location. "
                "Ajustar DriverEventsAdapter.handle_location_update() a la firma real."
            )

        return {"ok": True}

    async def handle_trip_status(self, dto: TripStatusUpdate) -> dict:
        """
        Ajustar al RideUseCase real.
        """
        if hasattr(self.ride_uc, "update_status"):
            await self.ride_uc.update_status(
                dto.trip_id,
                dto.status,
                dto.driver_id,
                dto.timestamp,
            )
        elif hasattr(self.ride_uc, "driver_update_trip_status"):
            await self.ride_uc.driver_update_trip_status(
                driver_id=dto.driver_id,
                trip_id=dto.trip_id,
                status=dto.status,
                timestamp=dto.timestamp,
            )
        else:
            raise AttributeError(
                "RideUseCase no expone update_status ni driver_update_trip_status. "
                "Ajustar DriverEventsAdapter.handle_trip_status() a la firma real."
            )

        return {"ok": True}
