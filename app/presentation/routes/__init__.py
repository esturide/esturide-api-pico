import time

import anyio.to_thread
from fastapi import APIRouter, HTTPException

from app.shared.scheme import StatusSuccess

root_router = APIRouter()


@root_router.get("/")
async def endpoint_status():
    return StatusSuccess()


@root_router.get("/no-async")
async def endpoint_async():
    def async_task():
        time.sleep(5)
        return "It's ok"

    result = await anyio.to_thread.run_sync(async_task)

    return {"result": result}


@root_router.get("/exceptions")
async def endpoint_exceptions():
    raise HTTPException(500, "Generic exception.")
