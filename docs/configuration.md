# VerityAI Environment Configuration Guide

This document defines the environment configuration architecture, variable specifications, conventions, and security boundaries across the VerityAI repository.

---

## 📌 Architecture & Design Principles

1. **Strict Boundary Separation**:
   - **Frontend Variables**: Prefixed with `VITE_` per Vite conventions. Bundled into client-side JS bundles and treated as **public**.
   - **Backend Variables**: Consumed by Python/FastAPI via Pydantic Settings. Kept server-side and **never exposed to browsers**.
2. **Safe Defaults for Local Development**:
   - Both frontend and backend work out-of-the-box using built-in safe defaults without requiring manual `.env` file creation.
3. **No Secrets in Version Control**:
   - Local `.env` files are excluded by [.gitignore](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/.gitignore).
   - Only safe template files ([frontend/.env.example](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/frontend/.env.example) and [backend/.env.example](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/.env.example)) are tracked in Git.
4. **Environment Isolation in Automated Testing**:
   - Automated tests instantiate configuration with isolated parameters (`_env_file=None`) to avoid interference from developers' ambient local environment files.

---

## 📋 Supported Configuration Variables

| Variable | Component | Purpose | Default | Required? | Public / Browser Exposed? |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `VITE_API_BASE_URL` | Frontend | Target URL for backend FastAPI service | `http://localhost:8000` | No | **Yes (Public)** |
| `APP_NAME` | Backend | Application title and service identifier | `"VerityAI API"` | No | No (Server only) |
| `API_VERSION` | Backend | Semantic version string | `"0.1.0"` | No | No (Server only) |
| `ENVIRONMENT` | Backend | Runtime mode (`development`, `test`, `production`) | `"development"` | No | No (Server only) |
| `API_V1_PREFIX` | Backend | Base route prefix for version 1 API | `"/api/v1"` | No | No (Server only) |
| `CORS_ORIGINS` | Backend | Allowed CORS client origins (JSON array or comma-separated) | `["http://localhost:5173", "http://127.0.0.1:5173"]` | No | No (Server only) |
| `LOG_LEVEL` | Backend | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) | `"INFO"` | No | No (Server only) |
| `DATABASE_URL` | Backend | Database connection URL | `"sqlite:///./data/verityai.db"` | No | No (Server only) |

---

## 📁 Environment File Conventions

| File | Purpose | Git Tracking |
| :--- | :--- | :--- |
| `frontend/.env.example` | Frontend variable template with safe placeholders | **Tracked** (Committed) |
| `frontend/.env.local` | Local developer frontend overrides (e.g., custom port) | **Ignored** (Never committed) |
| `backend/.env.example` | Backend variable template with safe placeholders | **Tracked** (Committed) |
| `backend/.env` | Local developer backend overrides (e.g., custom log level) | **Ignored** (Never committed) |
| `.env`, `.env.*` | Any root or nested local environment files | **Ignored** (Never committed) |

---

## 🚀 Creating Local Environment Files

### Frontend Setup
If you need to target a backend on a non-default port or host:

```bash
cd frontend
cp .env.example .env.local
```

Edit `frontend/.env.local`:
```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

### Backend Setup
If you need to configure custom CORS origins or enable debug logging:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```dotenv
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

## 🔒 Security Best Practices

- **Never place secrets in frontend variables**: Any variable prefixed with `VITE_` is compiled directly into browser JavaScript.
- **Never expose backend configuration wholesale**: API endpoints return specific response contracts ([RootResponse](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/schemas/common.py), [HealthResponse](file:///c:/Users/Manoj%20Kumar/Desktop/VerityAI/backend/app/schemas/common.py)) rather than dumping settings dictionaries.
- **Sanitized Error Responses**: Internal exceptions and validation errors are sanitized to prevent revealing paths, environment variables, or credentials.
- **Log Sanitization & Correlation IDs**: Logs use the standard format `[%(asctime)s] [%(levelname)s] [%(name)s] [%(request_id)s] %(message)s`. Client-supplied `X-Request-ID` headers are validated against `^[a-zA-Z0-9_\-]{1,64}$` to eliminate CRLF/log injection attacks. Malformed or excessively long headers are replaced with newly generated UUID4 IDs. Request bodies, auth headers, and cookies are never logged.
- **Production Environment Sourcing**: In production, environment variables should be injected by the runtime environment (container runtime, platform secrets manager, or CI/CD pipelines) rather than static files committed to source control.

---

## 🛠️ Troubleshooting Configuration Errors

1. **`Malformed VITE_API_BASE_URL: '...' is not a valid absolute URL`**:
   - Check `frontend/.env.local` or environment variables. The URL must be an absolute URI starting with `http://` or `https://`.
2. **`Invalid log_level: '...'`**:
   - `LOG_LEVEL` must be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` (case-insensitive).
3. **`api_v1_prefix must start with a forward slash '/'`**:
   - The prefix must begin with `/` (e.g. `/api/v1`) and must not end with a trailing slash.
4. **`Invalid cors_origins format`**:
   - Supply origins as a comma-separated list (`http://localhost:3000,http://localhost:5173`) or a JSON array (`'["http://localhost:3000"]'`).
