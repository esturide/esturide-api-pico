import contextlib

from fireo.models import Model

from app.shared.utils import async_task, define_async_task


class AsyncSessionRepository:
    def __init__(self):
        pass

    async def save(self, instance: Model):
        def save_instance(s):
            try:
                s.save()
            except TypeError:
                return False
            else:
                return True

        return await async_task(save_instance, instance)

    async def update(self, instance: Model):
        def update_instance(s):
            try:
                s.update()
            except TypeError:
                return False
            else:
                return True

        return await async_task(update_instance, instance)

    @contextlib.contextmanager
    async def session(self):
        @define_async_task
        def saver(s):
            try:
                s.save()
            except TypeError:
                return False
            else:
                return True

        yield saver
