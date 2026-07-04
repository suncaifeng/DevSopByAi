from __future__ import annotations

from typing import NoReturn

from codex_run import run_codex
from contracts import (
    ExecutionInput,
    ExecutionResult,
    OrchestratorState,
    RouteDecision,
    RunPolicy,
    can_repair_spec,
    can_retry_codex,
    validate_execution_input,
    validate_execution_result,
    validate_route_decision,
)
from routing_system import route_decision


def main(execution_input: ExecutionInput) -> OrchestratorState:
    input_errors = validate_execution_input(execution_input)
    if input_errors:
        raise ValueError("Execution input is not ready: " + "; ".join(input_errors))

    state = OrchestratorState(current_dsl=execution_input.dsl)
    policy = execution_input.run_policy

    while state.total_cycles < policy.max_total_cycles:
        print(
            f"\n[MAIN] cycle={state.total_cycles} "
            f"step={state.current_step} "
            f"spec_version={state.spec_version}"
        )

        result = run_codex(execution_input, state)
        _validate_or_stop_result(result)

        state.last_execution = result
        state.history.append(result)

        decision = route_decision(result, state, execution_input)
        _validate_or_stop_decision(decision)

        state.last_route = decision
        print(f"[ROUTER] route={decision.route} reason={decision.reason}")

        if decision.route == "SUCCESS":
            print("[MAIN] Execution completed successfully.")
            return state

        if decision.route == "RETRY_CODEX":
            _apply_retry_code_route(state, policy)
            continue

        if decision.route == "REPAIR_SPEC":
            _apply_repair_spec_route(state, policy)
            # The real spec repair hook will replace execution_input.dsl later.
            continue

        if decision.route == "REGENERATE_SPEC":
            print("[MAIN] Spec regeneration requires upstream spec pipeline.")
            return state

        if decision.route == "ASK_USER":
            print("[MAIN] User input is required before execution can continue.")
            return state

        if decision.route == "FATAL":
            print("[MAIN] Fatal route received. Stopping.")
            return state

        _unknown_route(decision)

    print("[MAIN] Max total cycles reached. Stopping.")
    return state


def _validate_or_stop_result(result: ExecutionResult) -> None:
    errors = validate_execution_result(result)
    if errors:
        raise ValueError("Execution result violates contract: " + "; ".join(errors))


def _validate_or_stop_decision(decision: RouteDecision) -> None:
    errors = validate_route_decision(decision)
    if errors:
        raise ValueError("Route decision violates contract: " + "; ".join(errors))


def _apply_retry_code_route(state: OrchestratorState, policy: RunPolicy) -> None:
    if not can_retry_codex(state, policy):
        print("[MAIN] Codex retry budget exceeded. Stopping.")
        state.total_cycles = policy.max_total_cycles
        return

    state.codex_retries += 1
    state.total_cycles += 1
    print("[MAIN] Retrying Codex with the same DSL.")


def _apply_repair_spec_route(state: OrchestratorState, policy: RunPolicy) -> None:
    if not can_repair_spec(state, policy):
        print("[MAIN] Spec repair budget exceeded. Stopping.")
        state.total_cycles = policy.max_total_cycles
        return

    state.spec_repairs += 1
    state.spec_version += 1
    state.total_cycles += 1
    print("[MAIN] Spec repair route accepted. Repair hook is not implemented yet.")


def _unknown_route(decision: RouteDecision) -> NoReturn:
    raise ValueError(f"Unknown route: {decision.route}")


if __name__ == "__main__":
    raise SystemExit(
        "Build an ExecutionInput and call main(execution_input). "
        "Direct demo execution is intentionally disabled."
    )
