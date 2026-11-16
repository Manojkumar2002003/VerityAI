# VerityAI Frontend Application

This directory contains the user interface for **VerityAI**, an AI-generated text detection platform. The frontend is built using **React**, **TypeScript**, **Vite**, and **Tailwind CSS**.

---

## 📌 Implementation Status (Sprint 1, Feature 1.2)

- **Current State**: Initial application shell, client-side routing, layout structure, and developer tooling are established.
- **Backend & ML Integration**: Backend API communication (FastAPI) and machine-learning text detection (DeBERTa-v3 / baselines) are **not yet implemented**. The current interface provides a preview foundation and placeholder workspace.
- **Probabilistic Disclaimer**: Automated AI text detection is fundamentally probabilistic and cannot definitively establish authorship.

---

## 📋 Prerequisites

- **Node.js**: `v20.0.0` or higher (verified on Node `v24.19.0`)
- **npm**: `v10.0.0` or higher (verified on npm `v11.17.0`)

---

## 🚀 Getting Started

All commands below should be executed from within the `frontend/` directory:

```bash
cd frontend
```

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables (Optional)

An example environment file is provided in [.env.example](.env.example):

```bash
# Windows PowerShell
cp .env.example .env
```

`VITE_API_BASE_URL` is reserved for future integration with the FastAPI backend (default: `http://localhost:8000`).

### 3. Start Local Development Server

```bash
npm run dev
```

The application will be accessible at:
- Local: [http://localhost:5173/](http://localhost:5173/)

---

## 🧪 Available Scripts

| Script | Purpose |
| :--- | :--- |
| `npm run dev` | Starts the Vite development server with Hot Module Replacement (HMR). |
| `npm run build` | Runs strict TypeScript type-checking (`tsc -b`) and produces an optimized production bundle in `dist/`. |
| `npm run preview` | Locally previews the production build output from `dist/`. |
| `npm run test` | Runs the test suite via **Vitest** in single-run CI mode (26 tests). |
| `npm run test:watch` | Runs Vitest in interactive watch mode for test-driven development. |
| `npm run test:coverage` | Measures code coverage via `@vitest/coverage-v8` and generates terminal & HTML reports. |
| `npm run lint` | Runs **ESLint 9** using flat configuration rules across all source files. |
| `npm run format:check`| Verifies code formatting with **Prettier** without modifying files. |
| `npm run format` | Automatically formats all TypeScript, TSX, CSS, and JSON files with Prettier. |

---

## 📁 Frontend Directory Structure

```text
frontend/
├── public/               # Static assets (favicons, SVG icons)
├── src/
│   ├── app/              # Core application bootstrap and routing
│   │   ├── App.tsx       # Root application component
│   │   ├── config.ts     # Client environment configuration & validation
│   │   ├── config.test.ts # Configuration unit tests
│   │   └── router.tsx    # React Router DOM configuration
│   ├── components/       # Reusable UI components
│   │   └── layout/       # Application shell components
│   │       ├── Header.tsx / Header.test.tsx
│   │       ├── Footer.tsx / Footer.test.tsx
│   │       └── Layout.tsx / Layout.test.tsx
│   ├── pages/            # Page-level view components
│   │   ├── HomePage.tsx / HomePage.test.tsx # Initial landing & workspace preview
│   │   └── NotFoundPage.tsx / NotFoundPage.test.tsx # Fallback 404 route component
│   ├── styles/           # Global styles and Tailwind CSS directives
│   │   └── index.css     # Tailwind entry point and focus styling
│   ├── test/             # Test configuration and utilities
│   │   ├── setup.ts      # Vitest and React Testing Library setup
│   │   └── test-utils.tsx # Shared MemoryRouter render helper
│   ├── App.test.tsx      # Application shell integration & navigation tests
│   └── main.tsx          # DOM root mounting entry point
├── .env.example          # Safe template for environment variables
├── .prettierrc           # Prettier formatting rules
├── .prettierignore       # Prettier ignore patterns
├── eslint.config.js      # ESLint 9 flat configuration
├── index.html            # HTML entry point
├── package.json          # Dependencies and script definitions
├── postcss.config.js     # PostCSS configuration for Tailwind CSS and Autoprefixer
├── tailwind.config.js    # Tailwind CSS theme extension and content globs
├── tsconfig.json         # Strict TypeScript compiler options
├── tsconfig.node.json    # TypeScript compiler options for Vite tooling
└── vite.config.ts        # Vite and Vitest configuration (with v8 coverage)
```
