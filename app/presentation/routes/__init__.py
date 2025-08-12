import asyncio
import time

import anyio.to_thread
from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.shared.scheme import StatusSuccess

root_router = APIRouter(
    tags=["Root router"]
)


@root_router.get("/")
async def endpoint_status():
    return StatusSuccess()
