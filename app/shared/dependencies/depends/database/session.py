from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.shared.dependencies.depends.database.cache import get_cache
from app.shared.dependencies.depends.database.sql import get_sql_db


def get_session_sql_db():
    engine = get_sql_db()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def get_session_sql_async_db():
    engine = get_sql_db()
    AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_session_redis_cache():
    cache = get_cache()

    try:
        yield cache
    finally:
        cache.close()
