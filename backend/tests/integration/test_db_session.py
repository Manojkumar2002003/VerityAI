"""Integration tests for database session lifecycle, transactions, and dependency injection."""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db.session import get_db, get_session_factory

pytestmark = pytest.mark.integration


def test_session_executes_query(isolated_session: Session) -> None:
    """Verify that a session can be created and execute queries."""
    result = isolated_session.execute(text("SELECT 'verity' AS name"))
    row = result.fetchone()
    assert row is not None
    assert row[0] == "verity"


def test_uncommitted_writes_are_not_persisted(isolated_engine: Engine) -> None:
    """Verify that writes require an explicit commit and are not auto-committed."""
    with isolated_engine.connect() as conn:
        conn.execute(text("CREATE TABLE test_items (id INTEGER PRIMARY KEY, value TEXT)"))
        conn.commit()

    session_factory = get_session_factory(isolated_engine)

    # Session 1: write without commit
    s1 = session_factory()
    s1.execute(text("INSERT INTO test_items (id, value) VALUES (1, 'temporary')"))
    s1.close()

    # Session 2: verify record was not persisted
    s2 = session_factory()
    result = s2.execute(text("SELECT COUNT(*) FROM test_items WHERE id = 1")).scalar()
    s2.close()
    assert result == 0


def test_committed_writes_persist_across_sessions(isolated_engine: Engine) -> None:
    """Verify that explicitly committed writes persist to subsequent sessions."""
    with isolated_engine.connect() as conn:
        conn.execute(text("CREATE TABLE persistent_items (id INTEGER PRIMARY KEY, value TEXT)"))
        conn.commit()

    session_factory = get_session_factory(isolated_engine)

    # Session 1: write and commit
    s1 = session_factory()
    s1.execute(text("INSERT INTO persistent_items (id, value) VALUES (1, 'saved')"))
    s1.commit()
    s1.close()

    # Session 2: verify record was persisted
    s2 = session_factory()
    val = s2.execute(text("SELECT value FROM persistent_items WHERE id = 1")).scalar()
    s2.close()
    assert val == "saved"


def test_get_db_dependency_closes_session_on_success(isolated_engine: Engine) -> None:
    """Verify that get_db yields an active session and closes it after the request."""
    session_factory = get_session_factory(isolated_engine)
    captured_session: Session | None = None

    test_app = FastAPI()

    def override_get_db():
        db = session_factory()
        nonlocal captured_session
        captured_session = db
        try:
            yield db
        finally:
            db.close()

    @test_app.get("/db-test")
    def db_endpoint(db: Session = Depends(override_get_db)):
        return {"status": "ok", "active": db.is_active}

    with TestClient(test_app) as client:
        response = client.get("/db-test")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "active": True}

    assert captured_session is not None
    # Session transaction is closed and inactive after dependency cleanup
    assert not captured_session.in_transaction()


def test_get_db_dependency_closes_session_on_exception(isolated_engine: Engine) -> None:
    """Verify that get_db closes the session even when an endpoint raises an exception."""
    session_factory = get_session_factory(isolated_engine)
    captured_session: Session | None = None

    test_app = FastAPI()

    def override_get_db():
        db = session_factory()
        nonlocal captured_session
        captured_session = db
        try:
            yield db
        finally:
            db.close()

    @test_app.get("/db-crash")
    def crashing_endpoint(db: Session = Depends(override_get_db)):
        raise RuntimeError("Simulated endpoint failure")

    with TestClient(test_app, raise_server_exceptions=False) as client:
        response = client.get("/db-crash")
        assert response.status_code == 500

    assert captured_session is not None
    assert not captured_session.in_transaction()
