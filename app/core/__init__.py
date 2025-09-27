import contextlib
import functools

import fireo
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.config import get_settings

DEFAULT_APP_NAME = "Esturide (p) API"


@functools.lru_cache()
def get_root_app() -> FastAPI:
    settings = get_settings()

    @contextlib.asynccontextmanager
    async def lifespan(_app: FastAPI):
        fireo.connection(from_file=settings.db_credential)
        yield

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
