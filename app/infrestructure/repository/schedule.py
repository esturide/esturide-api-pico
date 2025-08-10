from app.core.exception import InvalidRequestException
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.user import User
from app.shared.types.enum import RoleUser
from app.shared.utils import async_task


class ScheduleRepository:
    @staticmethod
    async def get_current(user: User, role: RoleUser = RoleUser.driver) -> ScheduleTravel:
        def filter_schedule_task_driver(u):
            return list(ScheduleTravel.collection
                        .filter(driver=u)
                        .order('-created')
                        .fetch())

        def filter_schedule_task_passenger(u):
            return list(ScheduleTravel.collection
                        .filter('passengers', 'array_contains', u)
                        .order('-created')
                        .fetch())

        all_schedule = []

        if role == RoleUser.driver:
            all_schedule = await async_task(filter_schedule_task_driver, user)
        elif role == RoleUser.passenger:
            all_schedule = await async_task(filter_schedule_task_passenger, user)
        else:
            raise InvalidRequestException("You cannot make the request with the current user role.")

        if len(all_schedule) == 0:
            raise InvalidRequestException("You currently have a pending trip.")

        return all_schedule[0]

    @staticmethod
    async def get_by_driver(user: User, limit=10) -> list[ScheduleTravel]:
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        def filter_schedule_task(u):
            return list(ScheduleTravel.collection
                        .filter(driver=u)
                        .order('-created')
                        .limit(limit)
                        .fetch())

        all_schedule = await async_task(filter_schedule_task, user)

        return all_schedule

    @staticmethod
    async def get_by_passenger(user: User, limit=10) -> list[ScheduleTravel]:
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        def filter_schedule_task(u):
            return list(ScheduleTravel.collection
                        .filter('driver', '==', u)
                        .order('-created')
                        .limit(limit)
                        .fetch())

        return await async_task(filter_schedule_task, user)

    @staticmethod
    async def get_all(limit=10):
        if limit <= 1:
            raise InvalidRequestException("Limit must be greater than 1.")

        def filter_schedule_task():
            return list(ScheduleTravel.collection
                        .order('-created')
                        .limit(limit)
                        .fetch())

        return await async_task(filter_schedule_task)

    @staticmethod
    async def save(schedule: ScheduleTravel):
        await async_task(lambda s: s.save(), schedule)

        return True

    @staticmethod
    async def update(schedule: ScheduleTravel):
        await async_task(lambda s: s.update(), schedule)

        return True
