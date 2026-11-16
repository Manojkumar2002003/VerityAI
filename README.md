# VerityAI

VerityAI is an AI-generated text detection platform designed to distinguish human-written text from AI-generated text using fine-tuned Transformer encoder architectures and robust statistical baselines.

---

## 📌 Project Overview & Goals

The primary goal of VerityAI is to deliver transparent, calibrated, and reliable detection of AI-generated content. Rather than providing ungrounded binary verdicts, VerityAI focuses on rigorous evaluation, probabilistic score calibration, and clear limitation disclosures.

- **Initial Scope**: English-only text detection. Future multi-lingual support will be evaluated in subsequent roadmap phases.
- **Current Project Status**: **Sprint 1 Complete (Features 1.1–1.8)**. Decoupled frontend UI shell, FastAPI backend foundation, SQLite persistence infrastructure, structured logging & health checks, comprehensive automated testing suites, and architecture documentation are fully operational. ML inference and text analysis pipelines are planned for Sprint 2.

---

## 🛠️ Technology Stack

### Implemented Foundation (Sprint 1)
- **Frontend**: React 18, TypeScript 5.7, Vite 6, Tailwind CSS 3.4, React Router DOM 6.28.
- **Backend API**: Python 3.12, FastAPI 0.115+, Pydantic v2, Pydantic Settings, Uvicorn.
- **Persistence**: SQLite with SQLAlchemy 2.x ORM engine, sessionmaker, and declarative base.
- **Testing & Quality**:
  - Backend: `pytest` 8.4, `pytest-cov` 7.1 (91% statement coverage).
  - Frontend: `Vitest` 2.1, `@vitest/coverage-v8` (100% statement coverage), React Testing Library, ESLint 9, Prettier.
- **Tooling & Orchestration**: Cross-platform unified quality runner ([scripts/run_checks.py](scripts/run_checks.py)).

### Planned ML Stack (Sprint 2 and Beyond)
- **Frameworks**: PyTorch, Hugging Face Transformers (`transformers`, `tokenizers`, `accelerate`).
- **Classical Baselines**: scikit-learn (TF-IDF feature extraction, Logistic Regression).
- **Model Candidates**: Fine-tuned `microsoft/deberta-v3-base` (primary candidate), `roberta-base` (comparative baseline).
- **Calibration**: Empirical score calibration (Platt scaling / temperature scaling).

---

## 📚 Technical Documentation & Architecture

Comprehensive technical specifications and operational guides are maintained in the [`docs/`](docs/) directory:

- 🏛️ **[System Overview](docs/system-overview.md)**: High-level overview, current boundaries, planned detection workflow, and probabilistic disclosures.
- 📐 **[Technical Architecture Specification](docs/architecture.md)**: Detailed architecture diagram, component interactions, request lifecycle, and endpoint contracts.
- ⚖️ **[Architecture Decisions (ADR 0001)](docs/decisions/0001-initial-architecture.md)**: Architecture Decision Record for foundational technology choices and calibration strategy.
- ⚙️ **[Environment Configuration Guide](docs/configuration.md)**: Supported environment variables, `.env` file conventions, and security boundaries.
- 💾 **[Database Architecture Guide](docs/database.md)**: SQLite engine, session management, `get_db` dependency injection, and test isolation.
- 🧪 **[Automated Testing Guide](docs/testing.md)**: Testing tiers, test authoring conventions, coverage baselines, and troubleshooting.
- 📁 **[Repository Structure Guide](docs/repository-structure.md)**: Directory responsibilities and architectural boundaries.

---

## 🔬 Model Development Approach (Planned)

VerityAI approaches AI text detection through systematic benchmarking, calibration, and iterative model validation:

1. **Primary Model Candidate**: Fine-tuned `microsoft/deberta-v3-base` encoder. DeBERTa-v3 offers disentangled attention and enhanced masked language modeling pre-training, making it well-suited for subtle stylistic and syntactic signals.
2. **Comparative Baselines**:
   - `roberta-base`: Robust masked language modeling baseline.
   - `TF-IDF + Logistic Regression`: Classical statistical baseline to quantify the performance gain of Transformer representations over n-gram distributions.
3. **Probability Calibration & Thresholding**: Raw model logits will be calibrated (e.g., Platt scaling or temperature scaling) to produce dependable confidence scores rather than uncalibrated overconfident predictions.
4. **Evaluation Metrics**: Comprehensive evaluation across out-of-distribution domains using ROC-AUC, Precision-Recall AUC, F1 score, and False Positive Rate at high True Positive Rate thresholds (e.g., FPR @ 95% TPR).

---

## 📚 Planned Research Datasets (Pending Validation)

The following public benchmark datasets are planned for research and evaluation:

- **HC3** (Human ChatGPT Comparison Corpus)
- **M4** (Multi-generator, Multi-domain, Multi-lingual dataset)
- **RAID** (Robust AI Detection benchmark)
- **TuringBench** (Benchmark for Turing test and generator attribution)

> **Status Notice**: All planned datasets are strictly **pending validation** regarding dataset access, licensing terms, domain suitability, and data leakage/overlap checks. Datasets are not downloaded or included in this repository phase.

---

## 📁 Repository Directory Guide

```text
verity-ai/
├── frontend/             # React + TypeScript UI, components, pages, client-side tests
├── backend/              # FastAPI application, REST endpoints, Pydantic schemas, DB layer
├── ml/                   # Machine learning pipelines (reserved for Sprint 2)
│   ├── data/             # Dataset manifests, metadata, and docs (raw data excluded)
│   ├── preprocessing/    # Cleaning, normalization, and tokenization logic
│   ├── training/         # Training scripts, configurations, and checkpoints
│   ├── evaluation/       # Benchmark harnesses, metrics, and error analysis
│   ├── inference/        # Model loading interfaces and prediction engines
│   └── calibration/      # Probability calibration and threshold analysis
├── tests/                # Automated testing suites
│   ├── unit/             # Unit tests (backend, frontend, ML utilities)
│   ├── integration/      # Integration tests across API routes and persistence
│   └── ml/               # Pipeline tests, tensor shape validations, and metric tests
├── docs/                 # Architectural specifications, ADRs, and technical guides
│   └── decisions/        # Architecture Decision Records (ADRs)
├── infra/                # Containerization (Docker), orchestration, and deployment configs
├── scripts/              # Developer automation scripts (e.g. scripts/run_checks.py)
├── .gitignore            # Git exclusion rules for environments, databases, and caches
├── .editorconfig         # Code formatting and style consistency rules
├── README.md             # Project overview, quickstart, and status
└── LICENSE               # Licensing terms notice (decision pending)
```

---

## ⚠️ Important Limitations

- **Probabilistic Nature**: AI text detection is fundamentally probabilistic and cannot provide definitive or legally conclusive proof of authorship.
- **False Positives**: Detectors risk misclassifying human-written text as AI-generated, especially for non-native English writers, structured writing, or short excerpts.
- **Evasion & Paraphrasing**: Content modified through paraphrasers, prompt engineering, or hybrid human-AI editing can evade detection.
- **No Detector Deployed Yet**: VerityAI is currently in the foundational architectural phase. No operational detector is currently implemented or exposed.

---

## 📊 Sprint 1 Status & Roadmap

| Area / Feature | Status | Implementation Details |
| :--- | :---: | :--- |
| **Repository Structure (1.1)** | **Implemented** | Modular multi-tier repository layout, strict `.gitignore` rules |
| **Frontend Foundation (1.2)** | **Implemented** | React 18 shell, Tailwind CSS, Vite 6, layout, 404 routing |
| **Backend Foundation (1.3)** | **Implemented** | FastAPI service, root endpoint, CORS, safe error handling |
| **Environment Config (1.4)** | **Implemented** | Pydantic Settings, `.env.example` templates, test isolation |
| **Database Foundation (1.5)** | **Implemented** | SQLite via SQLAlchemy 2.x engine, sessions, declarative Base |
| **Logging & Health Checks (1.6)** | **Implemented** | Request correlation IDs (`X-Request-ID`), liveness & readiness probes |
| **Testing Foundation (1.7)** | **Implemented** | 39 backend tests (91% cov), 26 frontend tests (100% cov), runner |
| **Architecture Docs (1.8)** | **Implemented** | System overview, architecture spec, ADR 0001, database guide |
| **ML Inference Engine** | **Planned (Sprint 2)** | Model candidate benchmark, tokenizer pipeline, inference service |
| **Text Analysis API** | **Planned (Sprint 2)** | Document-level & passage-level text analysis endpoints |
| **Persistence of Analyses** | **Planned (Later Sprint)** | User accounts, analysis history ORM models & migrations |

---

## 🚀 Quick Start Guide

### 1. Unified Quality Runner
Run all tests, linter, formatting checks, and build verification from repository root:
```bash
python scripts/run_checks.py            # Run all checks across backend and frontend
python scripts/run_checks.py --coverage # Run with coverage reports
```

### 2. Frontend Development
```bash
cd frontend
npm install
npm run dev            # Start local development server at http://localhost:5173/
npm test               # Run Vitest test suites (26 tests)
npm run test:coverage  # Generate v8 test coverage report (100% coverage)
npm run lint           # Check code quality (ESLint)
npm run format:check   # Verify code formatting (Prettier)
npm run build          # Compile TypeScript and generate production bundle
```
See [frontend/README.md](frontend/README.md) for full details.

### 3. Backend Development
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell (or source .venv/bin/activate on Unix)
python -m pip install -r requirements.txt
python -m app.db.init_db       # Initialize SQLite database and directory
uvicorn app.main:app --reload  # Start FastAPI server at http://localhost:8000/
pytest                         # Run automated test suite (39 tests)
pytest -m unit                 # Run unit tests only
pytest -m integration          # Run integration tests only
pytest --cov=app               # Run with terminal coverage report (91% coverage)
```
See [backend/README.md](backend/README.md) for full details.

---

## 📄 License

The formal software license for VerityAI is **pending** a decision by the repository owner and stakeholders to align with planned commercial objectives and third-party model/dataset requirements. See [LICENSE](LICENSE) for details.

