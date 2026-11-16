"""Explicit database initialization entry point.

Creates the database storage directory if required and emits DDL for registered
models. Non-destructive and idempotent.
"""

import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import Engine

from app.core.config import get_settings
from app.db.session import create_db_engine, get_engine
from app.models import Base

logger = logging.getLogger("verityai.db")


def ensure_parent_directory_exists(database_url: str) -> None:
    """Ensure the parent directory for a local file-based SQLite database exists.

    If database_url is in-memory or a remote service, this operation is a safe no-op.
    """
    if database_url.startswith("sqlite:///") and ":memory:" not in database_url:
        raw_path = database_url.replace("sqlite:///", "")
        file_path = Path(raw_path)
        if file_path.parent and str(file_path.parent) != ".":
            file_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info("Ensured database parent directory exists: %s", file_path.parent)


def init_db(engine: Optional[Engine] = None, database_url: Optional[str] = None) -> None:
    """Explicitly initialize the database schema and storage directories.

    Guarantees that parent storage directories are created and calls
    `Base.metadata.create_all(bind=target_engine)`. Safe for repeated execution.
    """
    settings = get_settings()
    target_url = database_url or settings.database_url

    ensure_parent_directory_exists(target_url)

    target_engine = engine or (create_db_engine(target_url) if database_url else get_engine())
    Base.metadata.create_all(bind=target_engine)
    logger.info("Initialized database schema on engine: %s", target_engine.url)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Initializing VerityAI database...")
    init_db()
    print("Database initialization completed successfully.")
