import functools

import google.auth

from google.cloud.sql.connector import Connector
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine

from app.core import get_settings


@functools.lru_cache()
def get_sql_db():
    settings = get_settings()

    credentials, project = google.auth.load_credentials_from_file(settings.google_application_credentials)
    connector = Connector(credentials=credentials)

    def getconn():
        conn = connector.connect(
            settings.db_sql_instance,
            "pg8000",
            user=settings.db_sql_user,
            password=settings.db_sql_password,
            db=settings.db_sql_name,
        )
        return conn

    return create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )


@functools.lru_cache()
def get_sql_async_db():
    settings = get_settings()

    credentials, project = google.auth.load_credentials_from_file(settings.google_application_credentials)
    connector = Connector(credentials=credentials)

    def getconn():
        conn = connector.connect(
            settings.db_sql_instance,
            "asyncpg",
            user=settings.db_sql_user,
            password=settings.db_sql_password,
            db=settings.db_sql_name,
        )

        return conn

    return create_async_engine(
        "postgresql+asyncpg://",
        creator=getconn,
    )
