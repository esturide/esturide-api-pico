from fastapi import BackgroundTasks

from app.domain.service.background.listener import ListenerService


class ScheduleTaskService:
    def __init__(self) -> None:
        pass

    def create_task(self, background_tasks: BackgroundTasks, listener: ListenerService):
        async def task():
            return await listener.task()

        background_tasks.add_task(task)
