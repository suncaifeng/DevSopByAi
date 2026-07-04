from __future__ import annotations

from contracts import (
    ExecutionErrorType,
    ExecutionInput,
    ExecutionResult,
    OrchestratorState,
    RouteDecision,
    can_repair_spec,
    can_retry_codex,
    contains_blocking_marker,
    is_none_section,
)


STUCK_LOOP_WINDOW = 3


def route_decision(
    result: ExecutionResult,
    state: OrchestratorState,
    execution_input: ExecutionInput,
) -> RouteDecision:
    """
    Decide the next route from execution evidence.

    This module is a routing adapter only:
    - no Codex execution
    - no spec mutation
    - no state mutation
    """

    if result.status == "SUCCESS":
        return RouteDecision(
            route="SUCCESS",
            reason="Codex execution returned SUCCESS",
            confidence=1.0,
            requires_spec_change=False,
            source_error_type=result.error_type,
        )

    if _dsl_has_blocking_state(execution_input):
        return RouteDecision(
            route="REPAIR_SPEC",
            reason="DSL contains blockers, unresolved issues, or blocking markers",
            confidence=0.95,
            requires_spec_change=True,
            source_error_type=result.error_type,
        )

    if _detect_stuck_loop(state, result.error_type):
        return _route_stuck_loop(result, state, execution_input)

    if result.error_type == "TEST_FAILURE":
        if can_retry_codex(state, execution_input.run_policy):
            return RouteDecision(
                route="RETRY_CODEX",
                reason="Test failure may be recoverable by another Codex execution",
                confidence=0.75,
                requires_spec_change=False,
                source_error_type=result.error_type,
            )
        return _repair_or_fail(
            result,
            state,
            execution_input,
            reason="Test failure persisted after retry budget",
        )

    if result.error_type == "SPEC_CONFLICT":
        return _repair_or_regenerate(
            result,
            state,
            execution_input,
            reason="Codex reported a spec conflict",
        )

    if result.error_type == "VALIDATION_ERROR":
        return _repair_or_fail(
            result,
            state,
            execution_input,
            reason="Execution result indicates validation failure",
        )

    if result.error_type == "CODEX_ERROR":
        if can_retry_codex(state, execution_input.run_policy):
            return RouteDecision(
                route="RETRY_CODEX",
                reason="Codex runtime error may be transient",
                confidence=0.65,
                requires_spec_change=False,
                source_error_type=result.error_type,
            )
        return RouteDecision(
            route="FATAL",
            reason="Codex runtime error exceeded retry budget",
            confidence=0.85,
            requires_spec_change=False,
            source_error_type=result.error_type,
        )

    if result.error_type == "ENV_ERROR":
        return RouteDecision(
            route="FATAL",
            reason="Environment error is not recoverable by rerunning Codex",
            confidence=0.9,
            requires_spec_change=False,
            source_error_type=result.error_type,
        )

    return RouteDecision(
        route="FATAL",
        reason="Unknown execution error type; stopping for safety",
        confidence=0.6,
        requires_spec_change=False,
        source_error_type=result.error_type,
    )


def _dsl_has_blocking_state(execution_input: ExecutionInput) -> bool:
    dsl = execution_input.dsl

    if contains_blocking_marker(dsl):
        return True

    if dsl.get("COMPILATION_STATUS") == "DSL_BLOCKED":
        return True

    if dsl.get("REPAIR_STATUS") == "REPAIR_BLOCKED":
        return True

    if not is_none_section(dsl.get("BLOCKERS")):
        return True

    if not is_none_section(dsl.get("UNRESOLVED_ISSUES")):
        return True

    return False


def _detect_stuck_loop(state: OrchestratorState, current_error: ExecutionErrorType) -> bool:
    recent_errors = [item.error_type for item in state.history[-(STUCK_LOOP_WINDOW - 1) :]]
    recent_errors.append(current_error)

    if len(recent_errors) < STUCK_LOOP_WINDOW:
        return False

    return all(error == recent_errors[0] for error in recent_errors)


def _route_stuck_loop(
    result: ExecutionResult,
    state: OrchestratorState,
    execution_input: ExecutionInput,
) -> RouteDecision:
    if result.error_type in {"TEST_FAILURE", "SPEC_CONFLICT", "VALIDATION_ERROR"}:
        return _repair_or_regenerate(
            result,
            state,
            execution_input,
            reason=f"Repeated {result.error_type} indicates a stuck execution loop",
        )

    return RouteDecision(
        route="FATAL",
        reason=f"Repeated {result.error_type} indicates an unrecoverable loop",
        confidence=0.9,
        requires_spec_change=False,
        source_error_type=result.error_type,
    )


def _repair_or_regenerate(
    result: ExecutionResult,
    state: OrchestratorState,
    execution_input: ExecutionInput,
    reason: str,
) -> RouteDecision:
    if can_repair_spec(state, execution_input.run_policy):
        return RouteDecision(
            route="REPAIR_SPEC",
            reason=reason,
            confidence=0.8,
            requires_spec_change=True,
            source_error_type=result.error_type,
        )

    return RouteDecision(
        route="REGENERATE_SPEC",
        reason=f"{reason}; spec repair budget exceeded",
        confidence=0.75,
        requires_spec_change=True,
        source_error_type=result.error_type,
    )


def _repair_or_fail(
    result: ExecutionResult,
    state: OrchestratorState,
    execution_input: ExecutionInput,
    reason: str,
) -> RouteDecision:
    if can_repair_spec(state, execution_input.run_policy):
        return RouteDecision(
            route="REPAIR_SPEC",
            reason=reason,
            confidence=0.75,
            requires_spec_change=True,
            source_error_type=result.error_type,
        )

    return RouteDecision(
        route="FATAL",
        reason=f"{reason}; spec repair budget exceeded",
        confidence=0.8,
        requires_spec_change=False,
        source_error_type=result.error_type,
    )
