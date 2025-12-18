from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

import socketio
from pydantic import BaseModel, Field, ValidationError

from app.realtime.auth_provider import get_auth_usecase
from app.realtime.adapters.driver_events_adapter import (
    DriverEventsAdapter,
    LocationUpdate,
    TripStatusUpdate,
)

logger = logging.getLogger("socket.driver")

class DriverLocationUpdateIn(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    timestamp: datetime
    accuracy: Optional[float] = Field(default=None, ge=0)


class TripStatusUpdateIn(BaseModel):
    trip_id: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)
    timestamp: datetime

def _normalize_role(role_obj: Any) -> str:
    if role_obj is None:
        return ""
    try:
        return str(role_obj).lower()
    except Exception:
        return ""


def _extract_user_code(user_obj: Any) -> int:
    candidates = ["code", "id", "user_code", "uid"]
    for attr in candidates:
        if hasattr(user_obj, attr):
            val = getattr(user_obj, attr)
            if val is not None:
                return int(val)
    raise ValueError("No se pudo extraer driver_id del usuario (campos probados: code/id/user_code/uid).")

class DriverNamespace(socketio.AsyncNamespace):

    def _adapter(self) -> DriverEventsAdapter:
        return DriverEventsAdapter()

    async def on_connect(self, sid: str, environ: dict, auth: Any):
        token = auth.get("token") if isinstance(auth, dict) else None

        if not token:
            logger.warning("CONNECT REJECT sid=%s reason=missing_token", sid)
            return False

        auth_uc = get_auth_usecase()

        ok = await auth_uc.check(token)
        if not ok:
            logger.warning("CONNECT REJECT sid=%s reason=invalid_token", sid)
            return False

        try:
            role = await auth_uc.get_session_role(token)
            role_norm = _normalize_role(role)
            if ("driver" not in role_norm) and ("conductor" not in role_norm):
                logger.warning("CONNECT REJECT sid=%s reason=not_driver role=%s", sid, role)
                return False
        except Exception as e:
            logger.warning("CONNECT REJECT sid=%s reason=role_check_failed err=%s", sid, str(e))
            return False

        try:
            user_obj, _current_role = await auth_uc.auth_service.get_user_credentials_from_token(token)
            driver_id = _extract_user_code(user_obj)
        except Exception as e:
            logger.warning("CONNECT REJECT sid=%s reason=cannot_extract_driver_id err=%s", sid, str(e))
            return False

        await self.save_session(sid, {
            "token": token,
            "role": str(role),
            "driver_id": driver_id,
        })

        await self.enter_room(sid, f"driver:{driver_id}")

        logger.info("CONNECT OK sid=%s driver_id=%s role=%s", sid, driver_id, role)
        await self.emit("driver:connected", {"ok": True, "driver_id": driver_id}, to=sid)

    async def on_disconnect(self, sid: str):
        sess = await self.get_session(sid)
        driver_id = sess.get("driver_id") if isinstance(sess, dict) else None
        logger.info("DISCONNECT sid=%s driver_id=%s", sid, driver_id)

    # -------------------------
    # Eventos
    # -------------------------

    async def on_location_update(self, sid: str, data: dict):
        sess = await self.get_session(sid)
        if not sess or "driver_id" not in sess:
            logger.warning("EVENT BLOCKED sid=%s event=location_update reason=no_session", sid)
            return

        try:
            payload = DriverLocationUpdateIn.model_validate(data)
        except ValidationError as e:
            logger.warning("VALIDATION ERROR sid=%s event=location_update err=%s", sid, e)
            await self.emit(
                "error:validation",
                {"event": "location_update", "detail": e.errors()},
                to=sid,
            )
            return

        driver_id = sess["driver_id"]

        adapter = self._adapter()
        try:
            result = await adapter.handle_location_update(
                LocationUpdate(
                    driver_id=driver_id,
                    lat=payload.lat,
                    lng=payload.lng,
                    timestamp=payload.timestamp,
                    accuracy=payload.accuracy,
                )
            )
        except Exception as e:
            logger.exception("LOCATION UPDATE failed sid=%s driver_id=%s err=%s", sid, driver_id, str(e))
            await self.emit(
                "error:server",
                {"event": "location_update", "message": "Internal error"},
                to=sid,
            )
            return

        await self.emit("driver:ack", {"event": "location_update", **result}, to=sid)

    async def on_trip_status(self, sid: str, data: dict):
        sess = await self.get_session(sid)
        if not sess or "driver_id" not in sess:
            logger.warning("EVENT BLOCKED sid=%s event=trip_status reason=no_session", sid)
            return

        try:
            payload = TripStatusUpdateIn.model_validate(data)
        except ValidationError as e:
            logger.warning("VALIDATION ERROR sid=%s event=trip_status err=%s", sid, e)
            await self.emit(
                "error:validation",
                {"event": "trip_status", "detail": e.errors()},
                to=sid,
            )
            return

        driver_id = sess["driver_id"]

        adapter = self._adapter()
        try:
            result = await adapter.handle_trip_status(
                TripStatusUpdate(
                    driver_id=driver_id,
                    trip_id=payload.trip_id,
                    status=payload.status,
                    timestamp=payload.timestamp,
                )
            )
        except Exception as e:
            logger.exception("TRIP STATUS failed sid=%s driver_id=%s err=%s", sid, driver_id, str(e))
            await self.emit(
                "error:server",
                {"event": "trip_status", "message": "Internal error"},
                to=sid,
            )
            return

        await self.emit("driver:ack", {"event": "trip_status", **result}, to=sid)
