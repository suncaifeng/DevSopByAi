from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, TypedDict


ValidationVerdict = Literal["PASS", "FAIL", "REQUIRES_REPAIR"]
CompilationStatus = Literal["DSL_READY", "DSL_BLOCKED"]
RepairStatus = Literal["REPAIR_COMPLETE", "REPAIR_BLOCKED"]
ExecutionStatus = Literal["SUCCESS", "FAILED"]
ExecutionErrorType = Literal[
    "NONE",
    "TEST_FAILURE",
    "SPEC_CONFLICT",
    "ENV_ERROR",
    "CODEX_ERROR",
    "VALIDATION_ERROR",
    "UNKNOWN",
]
Route = Literal[
    "SUCCESS",
    "RETRY_CODEX",
    "REPAIR_SPEC",
    "REGENERATE_SPEC",
    "ASK_USER",
    "FATAL",
]


class DSLCandidate(TypedDict, total=False):
    TASK: str
    INPUT_SCHEMA: list[dict[str, Any]]
    OUTPUT_SCHEMA: list[dict[str, Any]]
    MODULES: list[dict[str, Any]]
    DATA_FLOW: list[dict[str, Any]]
    EXECUTION_STEPS: list[dict[str, Any]]
    RULES: list[dict[str, Any]]
    ERROR_HANDLING: list[dict[str, Any]]
    ACCEPTANCE_TESTS: list[dict[str, Any]]
    BLOCKERS: list[dict[str, Any]] | str
    COMPILATION_STATUS: CompilationStatus
    UNRESOLVED_ISSUES: list[dict[str, Any]] | str
    REPAIR_STATUS: RepairStatus
    CHANGE_LOG: list[dict[str, Any]] | str


@dataclass
class CodexReadiness:
    ready: bool
    reason: str = ""


@dataclass
class ValidatorResult:
    verdict: ValidationVerdict
    confidence: float
    codex_readiness: CodexReadiness
    critical_issues: list[dict[str, Any]] = field(default_factory=list)
    high_risk_issues: list[dict[str, Any]] = field(default_factory=list)
    reason_summary: str = ""


@dataclass
class WorkspacePolicy:
    root: str
    allowed_paths: list[str] = field(default_factory=list)
    denied_paths: list[str] = field(default_factory=list)


@dataclass
class RunPolicy:
    max_total_cycles: int = 10
    max_codex_retries: int = 2
    max_spec_repairs: int = 1
    stop_on_unknown_route: bool = True


@dataclass
class ExecutionInput:
    dsl: DSLCandidate
    validator_result: ValidatorResult
    workspace: WorkspacePolicy
    run_policy: RunPolicy = field(default_factory=RunPolicy)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    ran: bool = False
    passed: bool | None = None
    command: str = ""
    details: str = ""


@dataclass
class ExecutionResult:
    status: ExecutionStatus
    exit_code: int
    error_type: ExecutionErrorType = "NONE"
    summary: str = ""
    logs: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    tests: TestResult = field(default_factory=TestResult)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteDecision:
    route: Route
    reason: str
    confidence: float
    requires_spec_change: bool = False
    next_action: str = ""
    source_error_type: ExecutionErrorType | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestratorState:
    total_cycles: int = 0
    codex_retries: int = 0
    spec_repairs: int = 0
    current_step: int = 0
    spec_version: int = 1
    current_dsl: DSLCandidate = field(default_factory=DSLCandidate)
    last_route: RouteDecision | None = None
    last_execution: ExecutionResult | None = None
    history: list[ExecutionResult] = field(default_factory=list)


def to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def is_none_section(value: Any) -> bool:
    return value == "NONE" or value == [] or value is None


def contains_blocking_marker(value: Any) -> bool:
    if isinstance(value, str):
        return "UNSPECIFIED_BLOCKING" in value or "AMBIGUITY_BLOCKING" in value

    if isinstance(value, dict):
        return any(contains_blocking_marker(item) for item in value.values())

    if isinstance(value, list):
        return any(contains_blocking_marker(item) for item in value)

    return False


def validate_dsl_candidate(dsl: DSLCandidate) -> list[str]:
    errors: list[str] = []

    required_sections = [
        "TASK",
        "INPUT_SCHEMA",
        "OUTPUT_SCHEMA",
        "MODULES",
        "DATA_FLOW",
        "EXECUTION_STEPS",
        "RULES",
        "ERROR_HANDLING",
        "ACCEPTANCE_TESTS",
        "BLOCKERS",
        "COMPILATION_STATUS",
        "UNRESOLVED_ISSUES",
        "REPAIR_STATUS",
        "CHANGE_LOG",
    ]

    for section in required_sections:
        if section not in dsl:
            errors.append(f"dsl.{section} is required")

    compilation_status = dsl.get("COMPILATION_STATUS")
    if compilation_status not in {"DSL_READY", "DSL_BLOCKED", None}:
        errors.append("dsl.COMPILATION_STATUS must be DSL_READY or DSL_BLOCKED")

    repair_status = dsl.get("REPAIR_STATUS")
    if repair_status not in {"REPAIR_COMPLETE", "REPAIR_BLOCKED", None}:
        errors.append("dsl.REPAIR_STATUS must be REPAIR_COMPLETE or REPAIR_BLOCKED")

    has_blocking_marker = contains_blocking_marker(dsl)
    blockers = dsl.get("BLOCKERS")
    unresolved = dsl.get("UNRESOLVED_ISSUES")

    if has_blocking_marker and compilation_status == "DSL_READY":
        errors.append("dsl.COMPILATION_STATUS cannot be DSL_READY while blocking markers exist")

    if not is_none_section(blockers) and compilation_status == "DSL_READY":
        errors.append("dsl.COMPILATION_STATUS cannot be DSL_READY while BLOCKERS is not NONE")

    if not is_none_section(unresolved) and repair_status == "REPAIR_COMPLETE":
        errors.append("dsl.REPAIR_STATUS cannot be REPAIR_COMPLETE while UNRESOLVED_ISSUES is not NONE")

    return errors


def validate_execution_input(execution_input: ExecutionInput) -> list[str]:
    errors: list[str] = []

    validator = execution_input.validator_result
    if validator.verdict != "PASS":
        errors.append("validator_result.verdict must be PASS before Codex execution")

    if not validator.codex_readiness.ready:
        errors.append("validator_result.codex_readiness.ready must be true")

    if not execution_input.dsl:
        errors.append("dsl must not be empty")
    else:
        errors.extend(validate_dsl_candidate(execution_input.dsl))

    if not execution_input.workspace.root:
        errors.append("workspace.root must not be empty")

    policy = execution_input.run_policy
    if policy.max_total_cycles < 1:
        errors.append("run_policy.max_total_cycles must be >= 1")

    if policy.max_codex_retries < 0:
        errors.append("run_policy.max_codex_retries must be >= 0")

    if policy.max_spec_repairs < 0:
        errors.append("run_policy.max_spec_repairs must be >= 0")

    return errors


def validate_execution_result(result: ExecutionResult) -> list[str]:
    errors: list[str] = []

    if result.status == "SUCCESS" and result.error_type != "NONE":
        errors.append("successful execution must use error_type NONE")

    if result.status == "FAILED" and result.error_type == "NONE":
        errors.append("failed execution must provide a non-NONE error_type")

    if result.exit_code == 0 and result.status == "FAILED":
        errors.append("failed execution should not use exit_code 0")

    if result.exit_code != 0 and result.status == "SUCCESS":
        errors.append("successful execution should use exit_code 0")

    if result.tests.ran and result.tests.passed is None:
        errors.append("tests.passed must be true or false when tests.ran is true")

    return errors


def validate_route_decision(decision: RouteDecision) -> list[str]:
    errors: list[str] = []

    if not 0 <= decision.confidence <= 1:
        errors.append("confidence must be between 0 and 1")

    if not decision.reason:
        errors.append("reason must not be empty")

    if decision.route in {"REPAIR_SPEC", "REGENERATE_SPEC"} and not decision.requires_spec_change:
        errors.append("spec-changing routes must set requires_spec_change to true")

    if decision.route in {"SUCCESS", "RETRY_CODEX"} and decision.requires_spec_change:
        errors.append("SUCCESS and RETRY_CODEX must not require spec change")

    return errors


def can_retry_codex(state: OrchestratorState, policy: RunPolicy) -> bool:
    return (
        state.total_cycles < policy.max_total_cycles
        and state.codex_retries < policy.max_codex_retries
    )


def can_repair_spec(state: OrchestratorState, policy: RunPolicy) -> bool:
    return (
        state.total_cycles < policy.max_total_cycles
        and state.spec_repairs < policy.max_spec_repairs
    )
