from app.shared.models.tracking import TrackingRecord
from app.shared.utils import async_task


class TrackingRepository:
    @staticmethod
    async def save(tracking: TrackingRecord) -> bool:
        def save_tracking(s):
            try:
                s.save()
            except TypeError:
                return False
            else:
                return True

        return await async_task(save_tracking, tracking)
