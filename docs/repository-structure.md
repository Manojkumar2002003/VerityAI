# VerityAI Repository Structure & Directory Responsibilities

This document defines the architectural boundaries and responsibilities for each directory within the VerityAI repository. Contributors must adhere to these boundaries to maintain a clean, modular, and maintainable codebase.

---

## Directory Overview

```text
verity-ai/
├── frontend/             # React + TypeScript user interface
├── backend/              # FastAPI application and core services
├── ml/                   # Machine learning pipelines and artifacts
│   ├── data/             # Dataset manifests, schemas, and metadata
│   ├── preprocessing/    # Cleaning, normalization, and tokenization logic
│   ├── training/         # Training scripts and configuration
│   ├── evaluation/       # Benchmark suites, evaluation metrics, and reports
│   ├── inference/        # Model loading and runtime prediction interfaces
│   └── calibration/      # Probability calibration and threshold analysis
├── tests/                # Automated testing suites
│   ├── unit/             # Unit tests (backend, frontend, ML utilities)
│   ├── integration/      # Integration and API contract tests
│   └── ml/               # Pipeline consistency, model tensor, and metric tests
├── docs/                 # Architectural and technical documentation
├── infra/                # Future deployment, containerization, and orchestration
├── scripts/              # Developer automation and maintenance scripts
├── .gitignore            # Git exclusion rules
├── .editorconfig         # Code style and formatting consistency rules
├── README.md             # Project overview and foundational documentation
└── LICENSE               # Licensing terms notice (pending formal decision)
```

---

## Detailed Directory Responsibilities

### `frontend/`
- **Purpose**: Houses the user-facing web application built with React and TypeScript.
- **Responsibilities**:
  - UI components, views, layouts, and style tokens.
  - Client-side state management and form handling.
  - API client communicating with backend endpoints.
  - Component-level unit and interaction tests.
- **Boundaries**: Must not perform direct database queries or heavy ML inference; communicates exclusively via the backend REST API.

### `backend/`
- **Purpose**: Houses the core application API built with FastAPI and Python.
- **Responsibilities**:
  - REST API endpoint routes and HTTP request handling.
  - Pydantic request/response schemas and input validation.
  - Application business logic and service layers.
  - Database persistence layer (initial support: SQLite).
  - Application configuration and environment variable loading.
- **Boundaries**: Must remain decoupled from frontend presentation logic and model training code. Accesses trained models solely through the ML inference interface.

### `ml/`
- **Purpose**: Contains the machine learning lifecycle components for AI text detection.
- **Subdirectories**:
  - `ml/data/`: Dataset manifests, split definitions, data documentation, and metadata. **Raw and processed dataset files must never be committed to Git.**
  - `ml/preprocessing/`: Text cleaning, normalization, linguistic segmentation, and tokenization logic.
  - `ml/training/`: Training routines, hyperparameter configurations, loss functions, and checkpoint management.
  - `ml/evaluation/`: Benchmark evaluation harnesses, metrics calculation (ROC-AUC, F1, FPR@95%TPR), error analysis, and reproducible experiment logs.
  - `ml/inference/`: Model loading routines, optimized runtime inference, batch prediction, and fallback strategies.
  - `ml/calibration/`: Score calibration (e.g., Platt scaling, isotonic regression) and decision-threshold tuning experiments.
- **Boundaries**: Code in `ml/` must be modular and testable without requiring web servers or UI dependencies.

### `tests/`
- **Purpose**: Comprehensive test suites ensuring correctness, reliability, and regression prevention.
- **Subdirectories**:
  - `tests/unit/`: Fast unit tests for isolated functions, schemas, utilities, and components.
  - `tests/integration/`: End-to-end API tests, database integration tests, and multi-service workflows.
  - `tests/ml/`: ML-specific tests covering pipeline idempotency, tensor dimension validation, tokenization edge cases, and deterministic metric calculations.
- **Boundaries**: Tests must not rely on uncommitted large data files or live network downloads unless specifically mocked.

### `docs/`
- **Purpose**: Centralized documentation for engineering, research, and architecture.
- **Responsibilities**:
  - System architecture diagrams and specifications.
  - API specifications and OpenAPI contract definitions.
  - Local setup, environment provisioning, and contribution guides.
  - Dataset cards, licensing reviews, and research experiment reports.
  - Model cards and detection limitation disclosures.

### `infra/`
- **Purpose**: Infrastructure as code, containerization, and deployment configurations.
- **Responsibilities**:
  - Dockerfiles for frontend, backend, and inference services.
  - Docker Compose configurations for local multi-container development.
  - CI/CD workflow manifests and deployment scripts.

### `scripts/`
- **Purpose**: Reusable utility scripts for developer productivity and repository maintenance.
- **Responsibilities**:
  - Repository bootstrapping and sanity checking scripts.
  - Data preparation and conversion utilities.
  - Database migration and maintenance helpers.
