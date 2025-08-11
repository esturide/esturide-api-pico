import anyio.to_thread


async def async_task(func, *args, **kwargs):
    return await anyio.to_thread.run_sync(func, *args, **kwargs)
