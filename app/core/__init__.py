import contextlib
import functools

import beanie
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.config import get_settings
from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.dependencies.depends.db import get_async_client_mongodb
from app.shared.models.ride import RideTravelModel
from app.shared.models.travel import ScheduleTravelModel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User

DEFAULT_APP_NAME = "Esturide (p) API"


@functools.lru_cache()
def get_root_app() -> FastAPI:
    settings = get_settings()

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI):
        async def init_db():
            client_db = get_async_client_mongodb()
            await client_db.admin.command("ping")

            await beanie.init_beanie(
                database=client_db["Customers"],
                document_models=[
                    User,
                ]
            )

            await beanie.init_beanie(
                database=client_db["Travels"],
                document_models=[
                    RideTravelModel,
                    ScheduleTravelModel,
                ]
            )

            await beanie.init_beanie(
                database=client_db["Tracking"],
                document_models=[
                    Tracking,
                ]
            )

            return client_db

        async def init_cache():
            client_cache = get_async_client_redis()

            await client_cache.ping()

            return client_cache

        db = await init_db()
        cache = await init_cache()

        yield

        await db.close()
        await cache.close()

    app = FastAPI(
        title=DEFAULT_APP_NAME,
        lifespan=lifespan,
    )

    origins = settings.allowed_origins

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
