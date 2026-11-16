"""SQLAlchemy engine, session factory, and FastAPI database session dependency."""

from typing import Any, Dict, Generator, Optional
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

# Module-level singletons (initialized on demand)
_engine: Optional[Engine] = None
_session_factory: Optional[sessionmaker[Session]] = None


def create_db_engine(database_url: Optional[str] = None) -> Engine:
    """Create a SQLAlchemy engine configured for the target database URL.

    Applies SQLite-specific connection arguments (such as check_same_thread=False)
    only when using a SQLite database URL.
    """
    url = database_url or get_settings().database_url
    connect_args: Dict[str, Any] = {}
    engine_kwargs: Dict[str, Any] = {}

    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        # Use StaticPool for in-memory SQLite instances to maintain persistence across threads
        if ":memory:" in url or url == "sqlite://":
            engine_kwargs["poolclass"] = StaticPool

    return create_engine(url, connect_args=connect_args, **engine_kwargs)


def get_engine() -> Engine:
    """Return or initialize the singleton database engine."""
    global _engine
    if _engine is None:
        _engine = create_db_engine()
    return _engine


def get_session_factory(engine: Optional[Engine] = None) -> sessionmaker[Session]:
    """Return a configured SQLAlchemy sessionmaker instance."""
    target_engine = engine or get_engine()
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=target_engine,
        expire_on_commit=False,
    )


def SessionLocal() -> Session:
    """Instantiate a new database session bound to the active engine."""
    global _session_factory
    if _session_factory is None:
        _session_factory = get_session_factory()
    return _session_factory()


def get_db() -> Generator[Session, None, None]:
    """FastAPI request dependency that provides an isolated database session.

    Yields a session and guarantees that it is closed when the request finishes,
    regardless of whether an exception occurred. Does not auto-commit writes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
