from __future__ import annotations

import json
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

from contracts import (
    ExecutionErrorType,
    ExecutionInput,
    ExecutionResult,
    OrchestratorState,
    TestResult,
)


DEFAULT_TIMEOUT_SECONDS = 300


def run_codex(execution_input: ExecutionInput, state: OrchestratorState) -> ExecutionResult:
    """
    Execute Codex with the validated DSL and return a contract-compliant result.

    This module is an execution adapter only:
    - no routing logic
    - no spec repair logic
    - no state mutation
    """

    run_id = str(uuid.uuid4())
    started_at = time.time()
    spec_path: Path | None = None

    try:
        spec_path = _write_temp_spec(run_id, execution_input)
        cmd = _build_codex_command(spec_path, execution_input)

        process = subprocess.run(
            cmd,
            cwd=execution_input.workspace.root,
            capture_output=True,
            text=True,
            timeout=_timeout_seconds(execution_input),
        )

        duration = time.time() - started_at
        stdout = process.stdout or ""
        stderr = process.stderr or ""
        exit_code = process.returncode

        status = "SUCCESS" if exit_code == 0 else "FAILED"
        error_type = "NONE" if status == "SUCCESS" else classify_error(stderr, stdout)

        return ExecutionResult(
            status=status,
            exit_code=exit_code,
            error_type=error_type,
            summary=_build_summary(status, error_type, exit_code),
            logs=_compact_logs(stdout, stderr),
            changed_files=[],
            tests=_extract_test_result(stdout, stderr),
            raw={
                "run_id": run_id,
                "duration": duration,
                "command": cmd,
                "spec_path": str(spec_path),
                "stdout": stdout,
                "stderr": stderr,
                "current_step": state.current_step,
                "total_cycles": state.total_cycles,
                "spec_version": state.spec_version,
            },
        )

    except subprocess.TimeoutExpired as exc:
        duration = time.time() - started_at
        stdout = exc.stdout or ""
        stderr = exc.stderr or "Codex execution timed out"

        return ExecutionResult(
            status="FAILED",
            exit_code=-1,
            error_type="CODEX_ERROR",
            summary="Codex execution timed out",
            logs=_compact_logs(stdout, stderr),
            changed_files=[],
            tests=TestResult(ran=False, passed=None),
            raw={
                "run_id": run_id,
                "duration": duration,
                "timeout_seconds": _timeout_seconds(execution_input),
                "spec_path": str(spec_path) if spec_path else "",
                "stdout": stdout,
                "stderr": stderr,
                "current_step": state.current_step,
                "total_cycles": state.total_cycles,
                "spec_version": state.spec_version,
            },
        )

    except FileNotFoundError as exc:
        return ExecutionResult(
            status="FAILED",
            exit_code=127,
            error_type="ENV_ERROR",
            summary="Codex command was not found",
            logs=[str(exc)],
            changed_files=[],
            tests=TestResult(ran=False, passed=None),
            raw={
                "run_id": run_id,
                "spec_path": str(spec_path) if spec_path else "",
                "current_step": state.current_step,
                "total_cycles": state.total_cycles,
                "spec_version": state.spec_version,
            },
        )

    finally:
        if spec_path is not None:
            _cleanup_temp_spec(spec_path)


def _write_temp_spec(run_id: str, execution_input: ExecutionInput) -> Path:
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f"codex_spec_{run_id}_",
        suffix=".json",
        delete=False,
    )

    with temp_file:
        json.dump(
            {
                "dsl": execution_input.dsl,
                "validator_result": {
                    "verdict": execution_input.validator_result.verdict,
                    "confidence": execution_input.validator_result.confidence,
                    "codex_readiness": {
                        "ready": execution_input.validator_result.codex_readiness.ready,
                        "reason": execution_input.validator_result.codex_readiness.reason,
                    },
                    "reason_summary": execution_input.validator_result.reason_summary,
                },
                "metadata": execution_input.metadata,
            },
            temp_file,
            ensure_ascii=False,
            indent=2,
        )

    return Path(temp_file.name)


def _build_codex_command(spec_path: Path, execution_input: ExecutionInput) -> list[str]:
    command = execution_input.metadata.get("codex_command")
    if isinstance(command, list) and command:
        return [str(part) for part in command] + ["--spec", str(spec_path)]

    return ["codex", "exec", "--spec", str(spec_path)]


def _timeout_seconds(execution_input: ExecutionInput) -> int:
    timeout = execution_input.metadata.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
    if isinstance(timeout, int) and timeout > 0:
        return timeout
    return DEFAULT_TIMEOUT_SECONDS


def _cleanup_temp_spec(spec_path: Path) -> None:
    try:
        spec_path.unlink(missing_ok=True)
    except OSError:
        pass


def classify_error(stderr: str, stdout: str) -> ExecutionErrorType:
    text = f"{stderr}\n{stdout}".lower()

    if "test" in text or "assert" in text or "pytest" in text:
        return "TEST_FAILURE"

    if "spec" in text and ("conflict" in text or "invalid" in text or "contract" in text):
        return "SPEC_CONFLICT"

    if "validation" in text or "validator" in text:
        return "VALIDATION_ERROR"

    if (
        "permission" in text
        or "not found" in text
        or "no such file" in text
        or "module not found" in text
        or "importerror" in text
        or "environment" in text
    ):
        return "ENV_ERROR"

    if (
        "timeout" in text
        or "traceback" in text
        or "syntaxerror" in text
        or "runtimeerror" in text
        or "exception" in text
    ):
        return "CODEX_ERROR"

    return "UNKNOWN"


def _build_summary(status: str, error_type: ExecutionErrorType, exit_code: int) -> str:
    if status == "SUCCESS":
        return "Codex execution completed successfully"
    return f"Codex execution failed with {error_type} and exit_code {exit_code}"


def _compact_logs(stdout: str, stderr: str) -> list[str]:
    logs: list[str] = []
    if stdout:
        logs.append(stdout)
    if stderr:
        logs.append(stderr)
    return logs


def _extract_test_result(stdout: str, stderr: str) -> TestResult:
    text = f"{stdout}\n{stderr}".lower()
    mentions_tests = "test" in text or "pytest" in text

    if not mentions_tests:
        return TestResult(ran=False, passed=None)

    failed = "failed" in text or "failure" in text or "assert" in text
    passed = not failed and ("passed" in text or "success" in text)

    return TestResult(
        ran=True,
        passed=passed,
        details="Test signal inferred from Codex output",
    )
