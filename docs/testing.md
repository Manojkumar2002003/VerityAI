# VerityAI Automated Testing Guide

This document details the automated testing architecture, directory organization, test layers, coverage reporting, quality checks, and troubleshooting procedures for the VerityAI repository.

---

## 📌 Testing Strategy & Architecture

VerityAI adopts a multi-tier testing strategy designed for rapid local feedback, reliable regression detection, and rigorous isolation:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Quality Assurance Layers                        │
├────────────────────────────────────────────────────────────────────────┤
│  1. Unit Tests                                                         │
│     - Backend: Isolated configuration, schema validation, logging      │
│     - Frontend: Component rendering, router links, utility functions   │
├────────────────────────────────────────────────────────────────────────┤
│  2. Integration Tests                                                  │
│     - Backend: FastAPI route handlers via TestClient, middleware,      │
│       exception sanitization, SQLite engine & transactional sessions   │
│     - Frontend: Shell navigation, routing, not-found fallbacks          │
├────────────────────────────────────────────────────────────────────────┤
│  3. ML Pipeline Tests (Reserved for Later Sprints)                     │
│     - Location: tests/ml/                                              │
│     - Future Scope: Tokenizer integrity, embedding shapes, calibrated   │
│       confidence scores, baseline metrics, model inference contracts   │
├────────────────────────────────────────────────────────────────────────┤
│  4. Static Analysis & Build Verification                               │
│     - ESLint (code quality and React hook rules)                       │
│     - Prettier (formatting style verification)                         │
│     - TypeScript (`tsc --noEmit`) & Vite production compilation        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Test Directory Organization

```text
verity-ai/
├── frontend/
│   └── src/
│       ├── app/
│       │   └── config.test.ts          # Client environment configuration unit tests
│       ├── components/layout/
│       │   ├── Header.test.tsx         # Header component unit tests
│       │   ├── Footer.test.tsx         # Footer component unit tests
│       │   └── Layout.test.tsx         # Layout structure integration tests
│       ├── pages/
│       │   ├── HomePage.test.tsx       # Landing page presentation unit tests
│       │   └── NotFoundPage.test.tsx   # 404 page presentation unit tests
│       ├── test/
│       │   ├── setup.ts                # JSDOM polyfills and afterEach cleanup
│       │   └── test-utils.tsx          # MemoryRouter render helper
│       └── App.test.tsx                # Application shell integration & navigation tests
├── backend/
│   ├── app/                            # Backend application package
│   ├── tests/
│   │   ├── conftest.py                 # Shared pytest fixtures & DB teardown
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_config.py          # Settings validation & CORS parsing unit tests
│   │   │   ├── test_logging.py         # Request ID generation & filter unit tests
│   │   │   └── test_schemas.py         # Pydantic response contract unit tests
│   │   └── integration/
│   │       ├── __init__.py
│   │       ├── test_root.py            # Root "/" endpoint integration tests
│   │       ├── test_health.py          # Liveness & database readiness (200/503) tests
│   │       ├── test_middleware.py      # X-Request-ID propagation & redaction tests
│   │       ├── test_errors.py          # 404, 422 validation, & safe 500 error tests
│   │       ├── test_db_connection.py   # SQLite engine & directory init tests
│   │       └── test_db_session.py      # Session lifecycle, commits & get_db tests
│   ├── pytest.ini                      # Pytest runner configuration & markers
│   └── .coveragerc                     # Coverage branch tracking & exclusions
├── tests/
│   └── ml/
│       └── .gitkeep                    # Reserved for future ML pipeline & metric tests
└── scripts/
    └── run_checks.py                   # Cross-platform unified quality & test runner
```

---

## 🚀 Unified Quality & Test Runner

Run all repository tests, linter, formatting checks, and build verification with a single command from the repository root:

```bash
# Run all quality checks across backend and frontend
python scripts/run_checks.py

# Run all checks with coverage reports generated
python scripts/run_checks.py --coverage

# Fast test run (skips frontend lint, format check, and production build)
python scripts/run_checks.py --fast

# Backend checks only
python scripts/run_checks.py --backend-only

# Frontend checks only
python scripts/run_checks.py --frontend-only
```

The script automatically locates the backend virtual environment, detects the platform (`Windows`, `Linux`, `macOS`), streams output, and generates a formatted status table with execution durations. It exits with code `0` on success and code `1` if any check fails.

---

## 🐍 Backend Testing (`pytest`)

### 1. Prerequisites
Activate the backend virtual environment:
```bash
cd backend
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
# or: source .venv/bin/activate # Linux / macOS
```

### 2. Standard Test Execution
```bash
# Run full backend test suite
python -m pytest

# Run only unit tests
python -m pytest tests/unit
# or using pytest markers:
python -m pytest -m unit

# Run only integration tests
python -m pytest tests/integration
# or using pytest markers:
python -m pytest -m integration

# Run with verbose output and short traceback
python -m pytest -v --tb=short
```

### 3. Coverage Reporting
Coverage is measured using `pytest-cov` configured via [.coveragerc](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/.coveragerc):
```bash
# Generate terminal coverage report with missing line numbers
python -m pytest --cov=app --cov-report=term-missing

# Generate interactive HTML coverage report
python -m pytest --cov=app --cov-report=html
```
The HTML report is written to `backend/htmlcov/index.html`.

### 4. Database Test Isolation
Backend database tests are guaranteed isolated by fixtures in [`backend/tests/conftest.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/tests/conftest.py):
- **Temporary SQLite Files**: Ambient and engine databases are written to isolated directories created by pytest's `tmp_path` fixture. Tests **never** write to `./data/verityai.db`.
- **Engine Singleton Teardown**: The singleton `_engine` and `_session_factory` references in `app.db.session` are reset before each test and safely `.dispose()`d during fixture teardown.
- **Rollback Guarantee**: The `isolated_session` fixture automatically rolls back uncommitted changes and closes sessions in a `finally` block.

---

## ⚛️ Frontend Testing (`Vitest`)

### 1. Prerequisites
Ensure dependencies are installed:
```bash
cd frontend
npm install
```

### 2. Standard Test Execution
```bash
# Run all frontend tests once (CI mode)
npm test

# Run tests in interactive watch mode (development mode)
npm run test:watch
```

### 3. Coverage Reporting
Frontend coverage is provided by `@vitest/coverage-v8` configured in [`frontend/vite.config.ts`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/vite.config.ts):
```bash
# Run tests and generate terminal + HTML coverage reports
npm run test:coverage
```
The HTML report is written to `frontend/coverage/index.html`.

### 4. Frontend Quality Checks
```bash
# Lint TypeScript and React rules
npm run lint

# Verify code formatting against Prettier rules
npm run format:check

# Auto-format files
npm run format

# Compile TypeScript and build production bundle
npm run build
```

---

## 📊 Measured Coverage Baseline

As of **Sprint 1, Feature 1.7**, the measured test coverage baseline across implemented code is:

| Component | Test Framework | Executable Lines / Stmts | Coverage % | Status |
| :--- | :--- | :---: | :---: | :--- |
| **Backend API (`app`)** | `pytest-cov` 7.x | 297 stmts | **91%** | 39 / 39 tests passing |
| **Frontend UI (`src`)** | `@vitest/coverage-v8` | 134 stmts | **100%** | 26 / 26 tests passing |

> **Coverage Policy**: Coverage measures which statements and branches were executed during tests. High coverage is a necessary baseline but does not substitute for testing domain edge cases, error conditions, and contract boundaries.

---

## 🏷️ Test Naming & Authoring Conventions

1. **Python Backend**:
   - Test files: `test_<module>.py` inside `tests/unit/` or `tests/integration/`.
   - Test functions: `test_<behavior_or_outcome>()` (e.g. `test_readiness_returns_503_when_database_check_fails`).
   - Grouping: Tag modules or test classes with `@pytest.mark.unit` or `@pytest.mark.integration`.
   - Pattern: Follow the **Arrange - Act - Assert** (AAA) structure.
2. **React Frontend**:
   - Component test files: `<ComponentName>.test.tsx` located directly adjacent to `<ComponentName>.tsx`.
   - Utility / config test files: `<module>.test.ts`.
   - Queries: Prioritize accessible queries: `getByRole`, `getByLabelText`, `getByText`. Avoid querying by implementation details or raw class names.
   - Routing: Use `renderWithRouter(<Component />)` from `src/test/test-utils` for components requiring React Router context.

---

## 🔬 Machine Learning Testing (`tests/ml/`)

The directory `tests/ml/` is established and tracked for subsequent ML sprint features:
- **Scope**: Pipeline data validations, tokenizer output checks, embedding tensor shapes, calibration curve assertions, and model metric threshold validations.
- **Current State**: Model inference and fine-tuning are deferred to subsequent sprints. In accordance with project discipline, **no empty or fake placeholder tests** are placed in this directory.

---

## 🛠️ Troubleshooting Common Test Issues

1. **`ModuleNotFoundError: No module named 'app'`**:
   - Ensure you are running pytest from within the `backend/` directory or using `python scripts/run_checks.py`.
   - Verify `pythonpath = .` is present in `backend/pytest.ini`.
2. **`StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated`**:
   - This is an upstream warning emitted by Starlette/FastAPI's TestClient and does not indicate test failure.
3. **Frontend tests fail with React Router Splat Warning**:
   - React Router v6 warns about upcoming v7 transition flags. These warnings are non-fatal.
4. **Database locked or file permission errors on Windows**:
   - The `test_env_setup` fixture in `conftest.py` automatically isolates database files inside pytest's `tmp_path` and disposes of engine connections during teardown.
