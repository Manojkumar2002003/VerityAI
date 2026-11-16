"""Pytest configuration and shared test fixtures for VerityAI backend."""

from pathlib import Path
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.core.config import get_settings
import app.db.session as db_session_module
from app.db.init_db import init_db
from app.db.session import create_db_engine, get_session_factory
from app.main import create_app


@pytest.fixture(autouse=True)
def test_env_setup(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Generator[None, None, None]:
    """Ensure tests run with consistent test environment settings and isolated storage.

    Cleans up any created ambient database file and resets engine singletons after each test.
    """
    test_db = tmp_path / "test_ambient.db"
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("APP_NAME", "VerityAI API")
    monkeypatch.setenv("API_VERSION", "0.1.0")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{test_db}")
    get_settings.cache_clear()

    # Reset session module singletons for test isolation
    db_session_module._engine = None
    db_session_module._session_factory = None

    yield

    # Teardown: dispose active singleton engine
    if db_session_module._engine is not None:
        db_session_module._engine.dispose()
        db_session_module._engine = None
    db_session_module._session_factory = None
    get_settings.cache_clear()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient instance configured for testing."""
    test_app = create_app()
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def tmp_db_url(tmp_path: Path) -> str:
    """Provide an isolated, temporary SQLite database URL for tests."""
    db_file = tmp_path / "isolated.db"
    return f"sqlite:///{db_file}"


@pytest.fixture
def isolated_engine(tmp_db_url: str) -> Generator[Engine, None, None]:
    """Provide an isolated SQLAlchemy engine bound to a temporary database file."""
    engine = create_db_engine(tmp_db_url)
    init_db(engine=engine, database_url=tmp_db_url)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def isolated_session(isolated_engine: Engine) -> Generator[Session, None, None]:
    """Provide a transactional SQLAlchemy session bound to the isolated engine."""
    session_factory = get_session_factory(isolated_engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
