# VerityAI Database Architecture & Persistence Guide

This document details the database foundation, connection lifecycle, ORM architecture, session management, and isolation patterns implemented in **VerityAI**.

---

## 📌 Technology Selection & Rationale

VerityAI adopts **SQLite** managed via **SQLAlchemy 2.x** for the initial persistence layer:

1. **Simplicity & Zero-Overhead Local Setup**: SQLite requires no external server process, external port allocation, or credentials, making onboarding and local development seamless and reliable across Windows, macOS, and Linux.
2. **ACID Compliance & Reliability**: SQLite delivers full transactional consistency (Atomicity, Consistency, Isolation, Durability) suitable for single-node deployments and local workflows.
3. **Deterministic Test Isolation**: Because SQLite databases are self-contained files, automated tests can spin up ephemeral, throwaway database instances in milliseconds using pytest's `tmp_path` fixture without cross-test contamination.
4. **SQLAlchemy 2.x Abstraction**: Using SQLAlchemy 2.x guarantees that when VerityAI transitions to a multi-user client-server database (such as PostgreSQL) in future enterprise phases, the application's ORM models and query logic require minimal refactoring.

---

## 🏗️ Architecture Components

```
┌──────────────────────────────────────────────────────────────┐
│                    SQLAlchemy 2.x Layer                      │
├──────────────────────────────────────────────────────────────┤
│  app.core.config.Settings.database_url                       │
│    └─ "sqlite:///./data/verityai.db"                         │
│                                                              │
│  app.db.session.create_db_engine(url)                        │
│    ├─ connect_args: {"check_same_thread": False}             │
│    └─ poolclass: StaticPool (if in-memory sqlite://)         │
│                                                              │
│  app.db.session.get_session_factory(engine)                  │
│    └─ sessionmaker(autocommit=False, autoflush=False)        │
│                                                              │
│  app.db.session.get_db() -> Generator[Session, None, None]  │
│    ├─ Yields active Session instance to FastAPI endpoint     │
│    └─ finally: session.close() guaranteed closure            │
│                                                              │
│  app.db.base.Base (DeclarativeBase)                          │
│    └─ Common declarative metadata base for future ORM models │
│                                                              │
│  app.db.init_db.init_db()                                    │
│    ├─ ensure_parent_directory_exists(database_url)           │
│    └─ Base.metadata.create_all(bind=engine)                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Storage Locations & Git Hygiene

- **Default Development Database**: [`backend/data/verityai.db`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/data/verityai.db).
- **Git Exclusion**: The entire `backend/data/` directory and all database artifacts (`*.db`, `*.sqlite`, `*.sqlite3`, `*.db-wal`, `*.db-shm`) are explicitly excluded from version control in [`.gitignore`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/.gitignore).
- **Directory Initialization**: The database directory is automatically verified and created on demand by [`ensure_parent_directory_exists()`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/db/init_db.py#L18).

---

## ⚙️ Explicit Database Initialization

To initialize or verify the database storage directory and registered schemas manually:

```bash
cd backend
python -m app.db.init_db
```

This command:
1. Reads `DATABASE_URL` from the active environment or defaults to `sqlite:///./data/verityai.db`.
2. Creates the parent folder (e.g. `backend/data`) if it does not already exist.
3. Calls `Base.metadata.create_all(bind=engine)`.
4. Executes safely and idempotently; running it multiple times does not corrupt or overwrite existing tables.

---

## 🔒 Session Management & FastAPI Dependency

Endpoints requiring database access declare a dependency on `get_db`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.get("/example")
def read_example(db: Session = Depends(get_db)):
    # db is an active SQLAlchemy Session
    ...
```

### Lifecycle Guarantees:
- **No Auto-Commit**: Sessions are configured with `autocommit=False`. Data writes require an explicit `db.commit()` call.
- **Guaranteed Cleanup**: A `finally` block in `get_db` ensures `db.close()` is executed immediately after response generation, releasing connection handles even if an unhandled exception occurred during endpoint execution.

---

## 🧪 Test Database Isolation

Database tests adhere to strict isolation principles implemented in [`backend/tests/conftest.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/tests/conftest.py):

1. **No Developer DB Contamination**: Tests never write to `./data/verityai.db`.
2. **Per-Test SQLite Files**: Each test using `tmp_db_url` or `isolated_engine` runs against an ephemeral database file created inside pytest's isolated `tmp_path`.
3. **Engine Teardown**: The `isolated_engine` fixture yields the engine and disposes of all pooled connection handles in `finally: engine.dispose()`.
4. **Ambient Teardown**: `conftest.py` resets module singletons (`_engine = None`, `_session_factory = None`) and calls `dispose()` during `test_env_setup` teardown.
5. **Transactional Rollback**: The `isolated_session` fixture guarantees `session.rollback()` and `session.close()` in `finally`.

---

## 📋 Current Implementation Status & Future Schema Evolution

### Current State (Sprint 1)
- **Zero Business Tables**: In accordance with Sprint 1 boundary discipline, `Base.metadata.tables` contains **no application-specific tables**.
- **No Persistence of Analysis Data**: Analysis records, passage scores, and user accounts are not yet modeled or persisted.

### Planned Evolution (Later Sprints)
1. **Domain Models**: Subsequent sprints will define declarative models inheriting from `Base` (e.g., `AnalysisJob`, `PassageResult`, `ModelAudit`).
2. **Schema Migrations**: Schema evolution tools (such as **Alembic**) will be introduced when production database migrations become necessary.
