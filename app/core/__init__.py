import contextlib
import functools
import random

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.config import get_settings
from app.shared.dependencies import get_async_cache
from app.shared.dependencies.depends.db import get_document_db


DEFAULT_APP_NAME = "Esturide (p) API"


@functools.lru_cache()
def get_root_app() -> FastAPI:
    settings = get_settings()

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI):
        get_document_db()

        redis = get_async_cache()
        await redis.ping()

        yield

        await redis.close()


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
