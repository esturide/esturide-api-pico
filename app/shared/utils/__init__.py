import anyio.to_thread


async def async_task(task, *args, **kwargs):
    return await anyio.to_thread.run_sync(task, *args, **kwargs)


def define_async_task(task):
    async def wrapper(*args, **kwargs):
        return anyio.to_thread.run_sync(task, *args, **kwargs)

    return wrapper
