# VerityAI Backend API Service

This directory contains the backend REST API service for **VerityAI**, an AI-generated text detection platform. Built with **Python 3.12**, **FastAPI**, **Pydantic v2**, and **SQLAlchemy 2.x**.

---

### 📌 Implementation Status (Sprint 1, Feature 1.7)

- **Current State**: 
  - FastAPI application structure, configuration management, health checks, and model contract endpoint.
  - Centralized standard library logging with configurable log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), structured format, and context-bound correlation IDs (`request_id`).
  - Request correlation ID middleware: validates/sanitizes client-supplied IDs, generates secure UUID4 IDs, measures request duration in ms using monotonic clock, logs request lifecycle, and attaches `X-Request-ID` response headers.
  - Liveness (`GET /api/v1/health`) confirming application responsiveness without DB access.
  - Readiness (`GET /api/v1/health/ready`) verifying database connectivity via bounded `SELECT 1`, returning HTTP 200 on success and HTTP 503 on database failure without leaking raw exceptions.
  - SQLite database foundation using **SQLAlchemy 2.x**: engine creation, session factory, `get_db` dependency, declarative `Base`, and idempotent initialization (`init_db`).
  - Comprehensive automated test suite with **39 tests** organized into isolated `tests/unit/` (15 tests) and `tests/integration/` (24 tests) suites with registered pytest markers (`unit`, `integration`), automated engine teardown, and **91% test coverage** via `pytest-cov`.
- **Unimplemented Capabilities**:
  - Machine-learning inference and model loading (DeBERTa-v3 / baselines) are **not yet connected**; model-info reports `not_configured`.
  - Application-specific ORM tables (analysis records, passage results, users) and migrations are deferred to subsequent features.
  - Text submission, analysis processing, and authentication are not yet implemented.
- **Probabilistic Nature**: Automated AI text detection is probabilistic and cannot definitively establish authorship.

---

## 📋 Prerequisites

- **Python**: `3.12.x` (verified on Python `3.12.4`, specified in [.python-version](.python-version))
- **pip**: Latest version recommended

---

## 🚀 Getting Started

All commands below should be executed from within the `backend/` directory:

```bash
cd backend
```

### 1. Create and Activate Virtual Environment

**Windows PowerShell**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt (cmd)**:
```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**Linux / macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the sample environment file:

```bash
cp .env.example .env
```

Settings available in [.env.example](.env.example):
- `APP_NAME`: Application title (default: `"VerityAI API"`)
- `API_VERSION`: API semantic version (default: `"0.1.0"`)
- `ENVIRONMENT`: Runtime environment (`development`, `test`, `production`)
- `API_V1_PREFIX`: API route prefix (default: `"/api/v1"`)
- `CORS_ORIGINS`: Allowed origins for frontend (default: `["http://localhost:5173", "http://127.0.0.1:5173"]`)
- `LOG_LEVEL`: Standard log level (default: `"INFO"`, supports `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `DATABASE_URL`: SQLite connection URL (default: `"sqlite:///./data/verityai.db"`)

### 4. Initialize Database (Optional)

The database storage directory and tables can be explicitly created via:

```bash
python -m app.db.init_db
```

This ensures the `./data` directory exists and creates all registered SQLAlchemy models. This command is safe to run repeatedly (idempotent).

### 5. Start Development Server

```bash
uvicorn app.main:app --reload
```

The API service will start on:
- Base API: [http://localhost:8000/](http://localhost:8000/)
- Swagger UI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📝 Logging & Request Correlation

### Centralized Logging Architecture
- **Standard Library**: Configured via `app.core.logging.setup_logging()`. Idempotent — prevents duplicate handlers across tests and restarts.
- **Log Format**: `[%(asctime)s] [%(levelname)s] [%(name)s] [%(request_id)s] %(message)s`
- **Correlation ID Filter**: Uses a Python `ContextVar` (`request_id_ctx_var`) attached to standard `logging.LogRecord` instances via `CorrelationIdFilter`. Logs issued within a request automatically display `[req_<uuid>]`, while non-request logs display `[-]`.
- **Validation & Sanitization**: Incoming `X-Request-ID` headers are validated against `^[a-zA-Z0-9_\-]{1,64}$`. Unsafe headers (containing newlines, control characters, or exceeding 64 chars) are rejected and replaced with a newly generated UUID4 hex ID to prevent log injection.
- **Privacy & Security**: Request middleware measures request duration monotonically and records HTTP method, sanitized path, status code, duration, and correlation ID. Request bodies, authorization headers, cookies, and sensitive query parameters are never logged.

---

## 🩺 Health Check Architecture

The service distinguishes between process availability (liveness) and dependency readiness:

1. **Liveness Check (`GET /api/v1/health`)**:
   - Confirms the FastAPI process is responsive.
   - Fast, non-blocking check that **does not** query SQLite.
   - Contract:
     ```json
     {
       "status": "ok",
       "service": "VerityAI API",
       "version": "0.1.0"
     }
     ```

2. **Readiness Check (`GET /api/v1/health/ready`)**:
   - Confirms the backend can perform operational tasks by verifying database connectivity.
   - Executes a lightweight, bounded `SELECT 1` query using the existing SQLAlchemy engine.
   - Returns **HTTP 200** when healthy:
     ```json
     {
       "status": "ready",
       "checks": {
         "database": "ok"
       }
     }
     ```
   - Returns **HTTP 503** when connectivity fails:
     ```json
     {
       "status": "not_ready",
       "checks": {
         "database": "unavailable"
       }
     }
     ```
   - Never exposes raw SQL errors, connection strings, or internal paths in the response. Full diagnostic tracebacks are kept securely in server logs.

3. **Model Information (`GET /api/v1/model-info`)**:
   - Contractually discloses detection model availability.
   - Currently returns `status: "not_configured"`, explicitly stating that ML detection is not ready.

---

## 💾 Database Architecture

- **Engine & Dialect**: SQLite via SQLAlchemy 2.x `create_engine`. Automatically configures `check_same_thread=False` and uses `StaticPool` for in-memory SQLite instances in tests.
- **Session Management**: Session factory created via `sessionmaker(autocommit=False, autoflush=False)`.
- **FastAPI Dependency (`get_db`)**: Yields an isolated database session and guarantees closure upon request completion via a `finally` block. Does not auto-commit transactions.
- **Declarative Base**: [app/db/base.py](app/db/base.py) exports `Base` (`DeclarativeBase`) from which future ORM models will inherit.
- **Test Isolation**: Database tests execute against temporary isolated SQLite files created per test run via pytest fixtures, keeping development data untouched.

---

## 📡 Available Endpoints

| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Service identification and operational confirmation | Implemented (HTTP 200) |
| `GET` | `/api/v1/health` | Process liveness probe (no DB query) | Implemented (HTTP 200) |
| `GET` | `/api/v1/health/ready` | Dependency readiness probe (verifies SQLite connectivity) | Implemented (HTTP 200 / 503) |
| `GET` | `/api/v1/model-info` | Detection model status and language capability contract | Implemented (`not_configured`) |

---

## 🧪 Running Automated Tests
 
 Run pytest from the `backend/` directory:
 
 ```bash
-pytest
+# Run full test suite
+python -m pytest
+
+# Run only unit tests
+python -m pytest tests/unit
+# or via marker:
+python -m pytest -m unit
+
+# Run only integration tests
+python -m pytest tests/integration
+# or via marker:
+python -m pytest -m integration
+
+# Measure test coverage with terminal summary
+python -m pytest --cov=app --cov-report=term-missing
+
+# Generate interactive HTML coverage report
+python -m pytest --cov=app --cov-report=html
 ```
 
-Or with Python module invocation:
-
-```bash
-python -m pytest
-```
-
-Configuration and options are maintained in [pytest.ini](pytest.ini).
+Configuration and markers are maintained in [pytest.ini](pytest.ini) and coverage options in [.coveragerc](.coveragerc). See [docs/testing.md](../docs/testing.md) for full testing documentation.
 
 ---
 
 ## 📁 Directory Structure
 
 ```text
 backend/
 ├── app/
 │   ├── __init__.py           # Application package
 │   ├── main.py               # Application factory, CORS, middleware, and error handlers
 │   ├── api/
 │   │   ├── __init__.py       # API router package
 │   │   └── v1/
 │   │       ├── __init__.py   # API v1 package
 │   │       └── router.py     # Liveness, readiness, and model-info route handlers
 │   ├── core/
 │   │   ├── __init__.py       # Core package
 │   │   ├── config.py         # Pydantic Settings and environment validation
 │   │   ├── logging.py        # Centralized logging setup and correlation ID filtering
 │   │   └── middleware.py     # HTTP request logging and correlation ID middleware
 │   ├── db/
 │   │   ├── __init__.py       # Database package
 │   │   ├── base.py           # SQLAlchemy 2.x DeclarativeBase
 │   │   ├── init_db.py        # Explicit database initialization CLI/function
 │   │   └── session.py        # Engine creation, sessionmaker, and get_db dependency
 │   ├── models/
 │   │   └── __init__.py       # Model registration package (exports Base)
 │   ├── schemas/
 │   │   ├── __init__.py       # Schemas package
 │   │   └── common.py         # Response models (Root, Health, Readiness, ModelInfo)
 │   └── services/
 │       └── __init__.py       # Service layer (business logic deferred)
 ├── tests/
-│   ├── conftest.py           # Pytest fixtures and isolated temporary DB setup
-│   ├── test_config.py        # Configuration and validation tests
-│   ├── test_db_connection.py # Engine, directory creation, and connectivity tests
-│   ├── test_db_session.py    # Session lifecycle, transaction, and get_db tests
-│   ├── test_errors.py        # 404 and exception sanitization tests
-│   ├── test_health.py        # Health, readiness (200 & 503), and model-info endpoint tests
-│   ├── test_logging.py       # Log level, idempotent setup, and correlation filter tests
-│   ├── test_middleware.py    # X-Request-ID propagation, duration, and redaction tests
-│   └── test_root.py          # Root endpoint tests
+│   ├── __init__.py           # Tests package initialization
+│   ├── conftest.py           # Pytest fixtures and isolated temporary DB setup
+│   ├── unit/                 # Unit test suite (@pytest.mark.unit)
+│   │   ├── __init__.py
+│   │   ├── test_config.py    # Configuration & CORS parsing unit tests
+│   │   ├── test_logging.py   # Request ID generation & filter tests
+│   │   └── test_schemas.py   # Pydantic schema validation tests
+│   └── integration/          # Integration test suite (@pytest.mark.integration)
+│       ├── __init__.py
+│       ├── test_db_connection.py # Engine, directory creation, & connectivity tests
+│       ├── test_db_session.py    # Session lifecycle, transactions, & get_db tests
+│       ├── test_errors.py        # 404, 422, & safe 500 error sanitization tests
+│       ├── test_health.py        # Liveness, readiness (200/503), & model-info tests
+│       ├── test_middleware.py    # X-Request-ID propagation & redaction tests
+│       └── test_root.py          # Root endpoint tests
 ├── .env.example              # Sample environment configuration
+├── .coveragerc               # Coverage configuration and exclusions
 ├── .python-version           # Target Python version specification (3.12.4)
 ├── pytest.ini                # Pytest configuration and options
-├── requirements.txt          # Pinned backend dependencies
+├── requirements.txt          # Backend dependencies (including pytest-cov)
 └── README.md                 # Setup and operational documentation
 ```
