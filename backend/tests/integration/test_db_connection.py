"""Integration tests for database engine creation, connectivity, and initialization."""

from pathlib import Path
import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.db.init_db import ensure_parent_directory_exists, init_db
from app.db.session import create_db_engine
from app.models import Base

pytestmark = pytest.mark.integration


def test_sqlite_engine_executes_simple_query(isolated_engine: Engine) -> None:
    """Verify that the configured SQLite engine connects and executes a basic SQL query."""
    with isolated_engine.connect() as connection:
        result = connection.execute(text("SELECT 1 AS test_val"))
        row = result.fetchone()
        assert row is not None
        assert row[0] == 1


def test_sqlite_engine_respects_configured_path(tmp_path: Path) -> None:
    """Verify that the engine creates and writes to the exact specified file path."""
    db_file = tmp_path / "custom_location" / "verity_test.db"
    db_url = f"sqlite:///{db_file}"

    ensure_parent_directory_exists(db_url)
    assert db_file.parent.exists()

    engine = create_db_engine(db_url)
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE ping (id INTEGER PRIMARY KEY)"))
            conn.commit()

        assert db_file.exists()
        assert db_file.stat().st_size > 0
    finally:
        engine.dispose()


def test_missing_parent_directory_created_on_init(tmp_path: Path) -> None:
    """Verify that init_db creates nested directories that do not already exist."""
    deep_dir = tmp_path / "deeply" / "nested" / "dir"
    db_file = deep_dir / "test_nested.db"
    db_url = f"sqlite:///{db_file}"

    assert not deep_dir.exists()

    init_db(database_url=db_url)

    assert deep_dir.exists()
    assert db_file.exists()


def test_repeated_initialization_is_idempotent(isolated_engine: Engine, tmp_db_url: str) -> None:
    """Verify that calling init_db repeatedly does not error and behaves idempotently."""
    init_db(engine=isolated_engine, database_url=tmp_db_url)
    init_db(engine=isolated_engine, database_url=tmp_db_url)

    with isolated_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_no_application_tables_created_prematurely() -> None:
    """Verify that in Feature 1.5 Base.metadata contains no premature business tables."""
    assert len(Base.metadata.tables) == 0
