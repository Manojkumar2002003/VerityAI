# ADR 0001: Initial Architecture and Foundation Technology Decisions

- **Status**: Accepted (Implemented for Foundation; Planned for ML/Inference)
- **Date**: October 2026
- **Context**: Sprint 1, VerityAI Platform Foundation

---

## 📌 Context and Problem Statement

VerityAI is being engineered as an English-language AI-generated text detection platform. The platform must eventually support user text submission, document uploads, real-time ML inference, granular passage highlighting, calibrated confidence reporting, and analysis persistence.

Sprint 1 requires establishing a reliable, maintainable repository foundation across frontend, backend, database, configuration, and testing without prematurely introducing complex production infrastructure.

---

## ⚖️ Key Architecture Decisions

### Decision 1: SQLite for Initial Persistence Layer
- **Decision**: Adopt SQLite via SQLAlchemy 2.x as the initial relational database.
- **Status**: **Implemented**
- **Rationale**:
  - Eliminates external database service setup for local development.
  - Full ACID compliance without network overhead.
  - High performance and fast, deterministic test isolation via throwaway file-based databases in `tmp_path`.
  - SQLAlchemy 2.x provides the ORM abstraction needed to transition to PostgreSQL in future enterprise deployments without rewriting models.
- **Consequences**: Concurrency is limited to SQLite's file-locking model (mitigated via `check_same_thread=False` and single-node architecture). Client-server databases are deferred until multi-user scaling demands it.

---

### Decision 2: FastAPI for Backend API Service
- **Decision**: Build the REST API backend using Python 3.12 and FastAPI.
- **Status**: **Implemented**
- **Rationale**:
  - Python is the primary ecosystem for modern machine learning (PyTorch, Transformers, scikit-learn).
  - FastAPI provides native async ASGI concurrency, automatic OpenAPI documentation, and strong Pydantic validation.
  - Native integration with Python `contextvars` enables lightweight request correlation ID (`X-Request-ID`) propagation without distributed tracing overhead.
- **Consequences**: The backend maintains clean separation between web HTTP concerns and future ML inference services.

---

### Decision 3: React + TypeScript + Vite for Frontend
- **Decision**: Build the web frontend as a Single-Page Application (SPA) using React 18, TypeScript, and Vite with Tailwind CSS.
- **Status**: **Implemented**
- **Rationale**:
  - Static SPA decoupling ensures the frontend can be served independently or integrated with any REST backend.
  - TypeScript enforces compile-time type safety across UI components, routing, and future API schemas.
  - Vite delivers sub-second Hot Module Replacement (HMR) and optimized rollup production bundles.
  - Tailwind CSS enables responsive, accessible design with zero runtime CSS overhead.
- **Consequences**: The frontend is decoupled from backend templating engines, allowing independent testing and development.

---

### Decision 4: Decoupled, Modular ML Architecture
- **Decision**: Isolate the ML detection engine behind strict Python interfaces rather than embedding model logic into API route handlers.
- **Status**: **Planned (Sprint 2)**
- **Rationale**:
  - Enables side-by-side benchmarking of candidate architectures (`microsoft/deberta-v3-base`, `roberta-base`, TF-IDF + Logistic Regression).
  - Allows swapping, quantization, or updating model weights without refactoring API contracts or frontend clients.
  - Keeps web processes lightweight; model loading and inference pipelines remain independently testable.
- **Consequences**: Requires defining explicit inference abstractions and serialization boundaries before implementing detection endpoints.

---

### Decision 5: Probabilistic Calibration and Inconclusive Verdicts Over Binary Classifications
- **Decision**: Require probability calibration (e.g., Platt scaling / temperature scaling) and provide an explicit "Inconclusive" outcome category rather than forcing binary AI/Human decisions.
- **Status**: **Planned (Sprint 2 & Calibration Phase)**
- **Rationale**:
  - AI text detection is fundamentally probabilistic; raw model logits are notoriously overconfident on out-of-domain text.
  - Binary verdicts generate dangerous false accusations against human writers, particularly non-native English speakers.
  - Communicating uncertainty honestly is essential for ethical adoption in educational and editorial environments.
- **Consequences**: The frontend and API schemas must represent calibrated probabilities, confidence bands, and inconclusive states rather than simple true/false flags.
