import functools

import fireo
import fireo.database

from app.core import get_settings


@functools.lru_cache
def get_document_db() -> fireo.database.Database:
    settings = get_settings()

    return fireo.connection(from_file=settings.db_firebase_credential)
