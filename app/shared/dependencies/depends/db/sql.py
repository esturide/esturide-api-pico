import functools

from sqlalchemy import create_engine, String, Column, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



@functools.lru_cache
def get_sql_db():
    engine = create_engine("",pool_pre_ping=True,pool_recycle=3600)
    meta = MetaData()
    con = engine.connect()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
