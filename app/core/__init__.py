import contextlib
import functools

import beanie
from aredis_om import Migrator
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.config import get_settings
from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.dependencies.depends.db import get_async_client_mongodb
from app.shared.models.ride import RideTravelModel
from app.shared.models.tracking import Tracking
from app.shared.models.travel import TravelDocument
from app.shared.models.user import UserDocument

DEFAULT_APP_NAME = "Esturide (p) API"


async def init_core_mongodb():
    client_db = get_async_client_mongodb()
    await client_db.admin.command("ping")

    await beanie.init_beanie(
        database=client_db["Customers"],
        document_models=[
            UserDocument,
        ]
    )

    await beanie.init_beanie(
        database=client_db["Travels"],
        document_models=[
            RideTravelModel,
            TravelDocument,
        ]
    )

    await beanie.init_beanie(
        database=client_db["Tracking"],
        document_models=[
            Tracking,
        ]
    )

    return client_db


async def init_core_redis():
    client_cache = get_async_client_redis()
    await client_cache.ping()

    await Migrator().run()

    return client_cache


@functools.lru_cache()
def get_root_app() -> FastAPI:
    settings = get_settings()

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI):
        db = await init_core_mongodb()
        cache = await init_core_redis()

        """
        schedules_task = ScheduleTaskService(cache)
        
        async for schedule in schedules_task.all():
            schedules_task.create_task(background_tasks, schedule)
        """

        yield

        await db.close()
        await cache.close()

    is_production = settings.is_production

    app = FastAPI(
        title=DEFAULT_APP_NAME,
        lifespan=lifespan,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json"
    )

    origins = settings.allowed_cors

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
        compresslevel=5
    )

    return app
