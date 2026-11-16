#!/usr/bin/env python3
"""VerityAI Unified Quality and Test Orchestration Runner.

Executes backend pytest suites, frontend Vitest suites, ESLint, Prettier formatting
verification, and TypeScript production build checks with timing and status summaries.
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import List, NamedTuple, Optional


class CheckResult(NamedTuple):
    name: str
    command: str
    duration: float
    passed: bool
    error_message: Optional[str] = None


def get_backend_python(repo_root: Path) -> str:
    """Find the backend virtual environment Python binary or fall back to sys.executable."""
    windows_venv = repo_root / "backend" / ".venv" / "Scripts" / "python.exe"
    posix_venv = repo_root / "backend" / ".venv" / "bin" / "python"

    if windows_venv.is_file():
        return str(windows_venv)
    if posix_venv.is_file():
        return str(posix_venv)
    return sys.executable


def get_npm_cmd() -> str:
    """Return npm executable for the current platform."""
    return "npm.cmd" if os.name == "nt" else "npm"


def run_command(name: str, cmd: List[str], cwd: Path) -> CheckResult:
    """Run an external command and record status and elapsed duration."""
    cmd_str = " ".join(cmd)
    print(f"\n[RUNNING] {name}...")
    print(f"Directory: {cwd}")
    print(f"Command:   {cmd_str}\n")

    start_time = time.perf_counter()
    try:
        result = subprocess.run(cmd, cwd=cwd)
        duration = time.perf_counter() - start_time
        passed = result.returncode == 0
        return CheckResult(
            name=name,
            command=cmd_str,
            duration=duration,
            passed=passed,
            error_message=None if passed else f"Exited with code {result.returncode}",
        )
    except FileNotFoundError as err:
        duration = time.perf_counter() - start_time
        return CheckResult(
            name=name,
            command=cmd_str,
            duration=duration,
            passed=False,
            error_message=f"Executable not found: {err}",
        )
    except Exception as exc:
        duration = time.perf_counter() - start_time
        return CheckResult(
            name=name,
            command=cmd_str,
            duration=duration,
            passed=False,
            error_message=str(exc),
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="VerityAI Unified Quality and Test Runner")
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate test coverage reports for backend and frontend",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run only tests, skipping lint, formatting, and build verification",
    )
    parser.add_argument(
        "--backend-only",
        action="store_true",
        help="Run only backend checks",
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Run only frontend checks",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    backend_dir = repo_root / "backend"
    frontend_dir = repo_root / "frontend"

    python_bin = get_backend_python(repo_root)
    npm_bin = get_npm_cmd()

    results: List[CheckResult] = []

    # 1. Backend Checks
    if not args.frontend_only:
        backend_cmd = [python_bin, "-m", "pytest"]
        if args.coverage:
            backend_cmd.extend(["--cov=app", "--cov-report=term-missing"])

        results.append(
            run_command(
                name="Backend Test Suite (pytest)",
                cmd=backend_cmd,
                cwd=backend_dir,
            )
        )

    # 2. Frontend Checks
    if not args.backend_only:
        frontend_test_cmd = [npm_bin, "run", "test:coverage" if args.coverage else "test"]
        results.append(
            run_command(
                name="Frontend Test Suite (Vitest)",
                cmd=frontend_test_cmd,
                cwd=frontend_dir,
            )
        )

        if not args.fast:
            results.append(
                run_command(
                    name="Frontend Lint (ESLint)",
                    cmd=[npm_bin, "run", "lint"],
                    cwd=frontend_dir,
                )
            )

            results.append(
                run_command(
                    name="Frontend Format Check (Prettier)",
                    cmd=[npm_bin, "run", "format:check"],
                    cwd=frontend_dir,
                )
            )

            results.append(
                run_command(
                    name="Frontend Production Build (TypeScript & Vite)",
                    cmd=[npm_bin, "run", "build"],
                    cwd=frontend_dir,
                )
            )

    # Print Summary Table
    total_duration = sum(r.duration for r in results)
    all_passed = all(r.passed for r in results)

    print("\n" + "=" * 70)
    print("                    VerityAI Quality Checks Summary")
    print("=" * 70)
    for r in results:
        status_label = "[PASS]" if r.passed else "[FAIL]"
        print(f" {status_label}  {r.name:<45} ({r.duration:.2f}s)")
        if not r.passed and r.error_message:
            print(f"         Reason: {r.error_message}")
    print("=" * 70)
    print(f" Total Elapsed Time: {total_duration:.2f}s")
    if all_passed:
        print(" [SUCCESS] All automated quality checks passed!")
    else:
        print(" [FAILURE] One or more quality checks failed. Review output above.")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
