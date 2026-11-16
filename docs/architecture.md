# VerityAI Technical Architecture Specification

This document details the software architecture, module design, lifecycle flows, and technology selections implemented in **Sprint 1** for the **VerityAI** text detection platform.

---

## 🏛️ System Architecture Diagram

The diagram below maps the concrete components implemented in Sprint 1 (solid lines) alongside the planned detection pipelines deferred to future sprints (dashed lines):

```mermaid
flowchart TD
    subgraph Client["Frontend Layer (React 18 + Vite)"]
        Browser[User Browser]
        Shell[Application Shell / Router]
        Pages[HomePage & NotFoundPage]
        LayoutComp[Header & Footer Layout]
        FEConfig[Frontend Config - config.ts]

        Browser --> Shell
        Shell --> LayoutComp
        LayoutComp --> Pages
        Shell -. Reads .-> FEConfig
    end

    subgraph API_GW["Backend API Layer (FastAPI 0.115+)"]
        MainApp[app/main.py - FastAPI Factory]
        MW[RequestLoggingMiddleware - Timing & X-Request-ID]
        CORS[CORSMiddleware]
        ErrHandlers[Exception Handlers - 404, 422, Safe 500]
        Router[APIRouter - app/api/v1/router.py]
        BEConfig[Settings - app/core/config.py]
        Logger[Logging - app/core/logging.py]

        MainApp --> CORS
        CORS --> MW
        MW --> Router
        MW --> ErrHandlers
        MainApp -. Loads .-> BEConfig
        MainApp -. Initializes .-> Logger
    end

    subgraph Endpoints["Active Endpoints (Sprint 1)"]
        RootRoute["GET / (Root Service Info)"]
        LiveRoute["GET /api/v1/health (Liveness)"]
        ReadyRoute["GET /api/v1/health/ready (Readiness)"]
        ModelInfoRoute["GET /api/v1/model-info (Model Contract)"]

        Router --> RootRoute
        Router --> LiveRoute
        Router --> ReadyRoute
        Router --> ModelInfoRoute
    end

    subgraph DataLayer["Persistence Layer (SQLAlchemy 2.x)"]
        Engine[create_db_engine - SQLite]
        SessionFac[sessionmaker - SessionLocal]
        GetDB[get_db Request Dependency]
        InitDB[init_db - Directory & Table Init]
        BaseORM[Base - DeclarativeBase]
        SQLiteFile[(SQLite Database - verityai.db)]

        ReadyRoute -->|SELECT 1 Bounded Check| Engine
        Engine --> SessionFac
        SessionFac --> GetDB
        Engine --> SQLiteFile
        InitDB --> Engine
    end

    subgraph FutureML["ML & Detection Pipeline (Planned - Deferred)"]
        DetEngine["Detection Engine (Planned)"]
        Models["Transformer Models (DeBERTa-v3 / Baselines)"]
        Calib["Probability Calibration (Platt / Isotonic)"]

        DetEngine -. Planned .-> Models
        Models -. Planned .-> Calib
    end

    %% Decoupled Boundary Links
    Shell -.->|Future HTTP Client Integration| MainApp
    Router -.->|Future Analysis Route| DetEngine
    ModelInfoRoute -. Discloses .->|Status: not_configured| FutureML
```

---

## 🎨 Frontend Architecture

### 1. Technology & Tooling Stack
- **Framework**: [React 18.3](https://react.dev/) using modern functional components and hooks.
- **Language**: [TypeScript 5.7](https://www.typescriptlang.org/) with strict compiler flags (`noImplicitAny`, `strictNullChecks`).
- **Build Tool**: [Vite 6](https://vitejs.dev/) providing rapid Hot Module Replacement (HMR) and optimized rollup production bundles.
- **Routing**: [React Router DOM 6.28](https://reactrouter.com/) using `createBrowserRouter` and Splat routing (`*`).
- **Styling**: [Tailwind CSS 3.4](https://tailwindcss.com/) with PostCSS, Autoprefixer, and custom glassmorphism styles in [`frontend/src/styles/index.css`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/src/styles/index.css).
- **Testing**: [Vitest 2.1](https://vitest.dev/), [React Testing Library 16.1](https://testing-library.com/), and [JSDOM 25](https://github.com/jsdom/jsdom).

### 2. Module Organization
```text
frontend/src/
├── app/
│   ├── App.tsx          # Root application component mounting RouterProvider
│   ├── config.ts        # Typed validation of VITE_ environment variables
│   ├── config.test.ts   # Configuration parsing and validation unit tests
│   └── router.tsx       # React Router route tree definition
├── components/layout/
│   ├── Header.tsx       # Brand banner, home link, and sprint badge
│   ├── Footer.tsx       # Focus descriptor & probabilistic disclaimer
│   └── Layout.tsx       # Responsive container with <Outlet />
├── pages/
│   ├── HomePage.tsx     # Landing hero, workspace preview, capability cards
│   └── NotFoundPage.tsx # Friendly 404 handler with return-home navigation
├── styles/
│   └── index.css        # Tailwind directives and design system tokens
└── test/
    ├── setup.ts         # JSDOM Request polyfill & cleanup after each test
    └── test-utils.tsx   # Custom renderWithRouter helper for isolated tests
```

### 3. Startup & Execution
1. HTML entry point [`frontend/index.html`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/index.html) loads `/src/main.tsx`.
2. [`src/main.tsx`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/src/main.tsx) mounts `<App />` into the `#root` DOM element in `React.StrictMode`.
3. [`src/app/App.tsx`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/src/app/App.tsx) binds `routes` into `RouterProvider`.
4. [`src/components/layout/Layout.tsx`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/src/components/layout/Layout.tsx) renders the header, sticky footer, and page outlet.
5. The frontend operates completely client-side in Sprint 1 without initiating unmocked network calls to the backend API.

---

## ⚙️ Backend Architecture

### 1. Technology & Framework Stack
- **Language**: Python 3.12 (verified on `3.12.4`).
- **Framework**: [FastAPI 0.115+](https://fastapi.tiangolo.com/) built on Starlette and ASGI.
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/) for request/response serialization.
- **Configuration**: `pydantic-settings` with type coercion and environment variable precedence.
- **Database ORM**: [SQLAlchemy 2.x](https://www.sqlalchemy.org/) with modern 2.0-style execution syntax (`session.execute(text(...))`).
- **Web Server**: [Uvicorn 0.32+](https://www.uvicorn.org/) ASGI server.

### 2. Module Responsibilities
- [`backend/app/main.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/main.py): Application factory `create_app()`, CORS middleware configuration, exception handler registration, and sub-router inclusion.
- [`backend/app/core/config.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/core/config.py): Pydantic Settings class `Settings` reading environment variables with safe defaults and LRU cached `get_settings()`.
- [`backend/app/core/logging.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/core/logging.py): Centralized logging configuration, `CorrelationIdFilter`, and `request_id_ctx_var` context storage.
- [`backend/app/core/middleware.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/core/middleware.py): HTTP middleware generating/propagating `X-Request-ID`, measuring duration via `time.perf_counter()`, logging lifecycle, and catching unhandled errors.
- [`backend/app/api/v1/router.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/api/v1/router.py): Route definitions for `/api/v1/health` (liveness), `/api/v1/health/ready` (readiness), and `/api/v1/model-info` (metadata).
- [`backend/app/db/session.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/db/session.py): SQLAlchemy engine factory, `SessionLocal` factory, and `get_db` FastAPI dependency.
- [`backend/app/db/base.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/db/base.py): Exports declarative `Base` (`DeclarativeBase`).
- [`backend/app/db/init_db.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/db/init_db.py): Idempotent database creation and storage directory provisioning.
- [`backend/app/schemas/common.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/schemas/common.py): Reusable response models (`RootResponse`, `HealthResponse`, `ReadinessResponse`, `ModelInfoResponse`, `ErrorDetail`).

---

## 🔄 Backend Request Lifecycle

Every HTTP request traverses an orchestrated, deterministic pipeline:

```
Incoming Request
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 1. RequestLoggingMiddleware (app/core/middleware.py)   │
│    - Extracts or generates UUID4 request ID            │
│    - Sanitizes client header (^[a-zA-Z0-9_\-]{1,64}$)  │
│    - Sets request_id_ctx_var (ContextVar)              │
│    - Starts monotonic clock (time.perf_counter())      │
└────────────────────────────────────────────────────────┘
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 2. CORSMiddleware (Starlette)                          │
│    - Validates Origin against configured cors_origins  │
│    - Handles OPTIONS preflight requests                │
└────────────────────────────────────────────────────────┘
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 3. FastAPI Routing & Input Validation                  │
│    - Resolves URL against route paths                  │
│    - Validates query params / bodies against Pydantic  │
│    - Raises RequestValidationError (HTTP 422) if invalid
└────────────────────────────────────────────────────────┘
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 4. Dependency Injection (e.g., get_db)                 │
│    - Yields managed SQLAlchemy Session                 │
│    - Guarantees session.close() in finally block       │
└────────────────────────────────────────────────────────┘
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 5. Endpoint Execution                                  │
│    - /api/v1/health: Returns 200 HealthResponse (no DB)│
│    - /api/v1/health/ready: Runs SELECT 1 check on DB   │
│    - /api/v1/model-info: Returns model contract        │
└────────────────────────────────────────────────────────┘
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ 6. Response & Error Interception                       │
│    - Unhandled exceptions mapped to safe HTTP 500      │
│    - No stack traces or secrets returned to client     │
│    - X-Request-ID header attached to response          │
│    - Structured log emitted: METHOD PATH - STATUS (ms) │
└────────────────────────────────────────────────────────┘
      │
      ▼
Client Response (with X-Request-ID header)
```

---

## 🩺 Health Check & Monitoring Architecture

VerityAI maintains a clear separation between **process availability (liveness)** and **dependency readiness**:

| Endpoint | Probe Type | Checked Dependencies | HTTP Status Codes | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `GET /api/v1/health` | **Liveness** | None (pure in-memory check) | `200 OK` | Verifies the web process is running and responding. |
| `GET /api/v1/health/ready` | **Readiness** | SQLite connectivity (`SELECT 1`) | `200 OK`, `503 Service Unavailable` | Verifies dependencies required for operations are healthy. |
| `GET /api/v1/model-info` | **Metadata** | Model candidate contract | `200 OK` | Discloses model status (`not_configured`), confirming detection is not ready. |

---

## 📊 Sprint 1 Deliverables & Status Matrix

| Component Area | Sprint 1 Deliverable | Status | Verification Reference |
| :--- | :--- | :---: | :--- |
| **Repository Structure** | Modular multi-tier directory structure (Feature 1.1) | **Implemented** | [`docs/repository-structure.md`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/docs/repository-structure.md) |
| **Frontend Foundation** | React 18, Vite 6, Tailwind CSS, Layout shell (Feature 1.2) | **Implemented** | [`frontend/src/App.test.tsx`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/src/App.test.tsx) (26 tests passing) |
| **Backend Foundation** | FastAPI REST service, root, CORS, error handlers (Feature 1.3) | **Implemented** | [`backend/app/main.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/main.py) |
| **Configuration** | Pydantic Settings, environment templates, test isolation (Feature 1.4) | **Implemented** | [`docs/configuration.md`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/docs/configuration.md) |
| **Database Foundation** | SQLite via SQLAlchemy 2.x, engine, sessions, `init_db` (Feature 1.5) | **Implemented** | [`docs/database.md`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/docs/database.md) |
| **Logging & Health** | Standard logging, `X-Request-ID`, liveness & readiness (Feature 1.6) | **Implemented** | [`backend/app/core/logging.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/core/logging.py) |
| **Testing Foundation** | Unit/integration testing, 91% backend / 100% frontend coverage (Feature 1.7) | **Implemented** | [`docs/testing.md`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/docs/testing.md), [`scripts/run_checks.py`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/scripts/run_checks.py) |
| **Architecture Docs** | Comprehensive system and technical documentation (Feature 1.8) | **Implemented** | [`docs/architecture.md`](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/docs/architecture.md) |
| **ML Inference Engine** | PyTorch / DeBERTa-v3 model loading and prediction | **Planned (Sprint 2)** | Deferred per roadmap |
| **Text Analysis API** | `/api/v1/analyze` document and passage endpoints | **Planned (Sprint 2)** | Deferred per roadmap |
| **Analysis Persistence** | User accounts, analysis history ORM tables | **Planned (Later Sprint)** | Deferred per roadmap |
