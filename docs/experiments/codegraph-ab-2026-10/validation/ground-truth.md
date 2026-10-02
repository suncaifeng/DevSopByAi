# Independent blinded validation ground truth

- Final validation revision: 2; completed at 2026-10-02T05:48:03Z.
- Validation contexts: 4 fresh ephemeral Codex sessions, one per Q, all at `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`; no CodeGraph MCP configuration.
- Each ground truth below was derived from checked-in source/Git and local Python documentation for Q4. CodeGraph results were not used as ground truth.
- The first validation input/output set is retained under `round1/` and superseded because its sanitizer altered a valid TaskContract filename. Revision 2 preserved tracked paths and used newly randomized labels.
- The operator separately audited all 16 raw Codex JSONL event streams: no test-runner command was invoked; every measured worktree was clean before and after. Validators could not establish those session-local facts from source alone.

## Q1

At commit 37bc219ae4f5989d0bfaf6bfb917ae86108d33e1, the public Python entry point is main.main(execution_input) in main.py:21. It calls contracts.validate_execution_input before creating OrchestratorState; then loops, calls codex_run.run_codex, validates the result, appends it to history, calls routing_system.route_decision, validates the decision, and applies its route. The checked-in __main__ guard exits with instructions to construct ExecutionInput and call main directly (main.py:118-122). The tracked tree has no CLI/API wrapper or in-repository caller of main.

The adapter writes a temporary JSON spec, builds either the metadata-supplied command plus --spec or the default codex exec --spec command, and calls subprocess.run with workspace.root as cwd, captured text output, and a timeout (codex_run.py:36-46, 126-170). A normal return uses the exit code for SUCCESS/FAILED; failures are classified from output text. Logs, heuristic test signals, raw run data, and an empty changed_files list are returned. Timeout and FileNotFoundError have separate result branches, and the temporary spec is cleaned up in finally (codex_run.py:48-123, 173-243). The FileNotFoundError handler is source-confirmed; the source alone does not establish which underlying operation caused a particular runtime exception.

Routing checks SUCCESS first, then DSL blocking state, then the stuck-loop detector, then error-specific branches (routing_system.py:33-118). Blocking state includes blocking markers, DSL_BLOCKED or REPAIR_BLOCKED statuses, and BLOCKERS or UNRESOLVED_ISSUES values not considered NONE by contracts.is_none_section (routing_system.py:121-139; contracts.py:135-149). This is broader than checking only nonempty lists. The stuck-loop detector reads the last two history entries and appends the current error; since main appends the current result before calling the router, two identical consecutive failed executions can satisfy its three-item comparison (main.py:39-42; routing_system.py:142-149).

Retry and repair decisions use contracts.can_retry_codex and contracts.can_repair_spec in both the router and main's route helpers (routing_system.py:54-94, 180-219; main.py:91-110; contracts.py:270-281). Retry increments retry and cycle counts. Repair increments repair, spec_version, and cycle counts, but the repair hook is explicitly unimplemented; the adapter serializes execution_input.dsl, and main does not replace that input DSL. REGENERATE_SPEC, ASK_USER, FATAL, and SUCCESS return state; unknown routes raise ValueError; exhausting the cycle loop also returns state (main.py:48-76, 102-115). ASK_USER is declared and handled, but route_decision does not emit it.

The adapter infers test status from output text; it does not invoke a separate test runner (codex_run.py:229-243). Result validation checks that tests.passed is not None when tests.ran is true, but does not perform a runtime boolean-type check (contracts.py:231-249). No tests or other in-repository consumers of main are present in the tracked tree.

### Required dependencies
- **D1** (critical): `contracts.py::validate_execution_input` — main calls this before state initialization or execution dispatch; it gates readiness, DSL, workspace-root, and run-policy validation. Evidence: main.py:main:21-24 calls contracts.validate_execution_input; contracts.py:validate_execution_input:200-228
- **D2** (critical): `codex_run.py::run_codex` — main dispatches each execution cycle to this adapter. Evidence: main.py:main:36; codex_run.py:run_codex:22-75
- **D3** (critical): `contracts.py::validate_execution_result` — main validates each adapter result before saving it or routing it. Evidence: main.py:_validate_or_stop_result:79-82; contracts.py:validate_execution_result:231-249
- **D4** (critical): `routing_system.py::route_decision` — main passes the result, state, and input to this routing function after recording the result. Evidence: main.py:main:39-43; routing_system.py:route_decision:19-118
- **D5** (critical): `contracts.py::validate_route_decision` — main validates each routing result before applying its route. Evidence: main.py:_validate_or_stop_decision:85-88; contracts.py:validate_route_decision:252-267
- **D6** (critical): `contracts.py::can_retry_codex and can_repair_spec` — main's retry and repair handlers use these cross-file budget checks before incrementing counters. Evidence: main.py:_apply_retry_code_route:91-110; contracts.py:can_retry_codex:270-274; contracts.py:can_repair_spec:277-281
- **D7** (critical): `contracts.py::can_retry_codex and can_repair_spec` — routing_system uses the shared budget checks to choose retry, repair, regeneration, or failure routes. Evidence: routing_system.py:route_decision:54-94; routing_system.py:_repair_or_regenerate:174-195; routing_system.py:_repair_or_fail:198-219; contracts.py:can_retry_codex:270-274; contracts.py:can_repair_spec:277-281
- **D8** (critical): `contracts.py::contains_blocking_marker and is_none_section` — routing_system uses these contract helpers to evaluate DSL blocking markers, blockers, and unresolved issues. Evidence: routing_system.py:_dsl_has_blocking_state:121-139; contracts.py:contains_blocking_marker:139-149; contracts.py:is_none_section:135-136
- **D9** (critical): `contracts.py::ExecutionInput, OrchestratorState, ExecutionResult, TestResult, RouteDecision` — These data contracts carry input, execution evidence, orchestration history, and route decisions across the adapter, main loop, and router. Evidence: contracts.py:ExecutionInput:78-85; contracts.py:ExecutionResult:95-105; contracts.py:RouteDecision:107-115; contracts.py:OrchestratorState:118-129; codex_run.py:10-16, 56-75

### Tests and runtime notes

No tests are checked into this commit: the tracked tree contains the four Python modules, documentation files, and no test files. The only Python matches for test-related names are adapter test-signal extraction/classification code. No in-repository caller of main was found; main.py's direct-execution guard is the only checked-in direction for invoking it.
- No Python program, subprocess, or tests were run. Subprocess result branches are established from checked-in control flow, not observed runtime outcomes.
- The adapter catches FileNotFoundError around spec creation and subprocess invocation; source inspection confirms the handler's result, but not that every occurrence would mean the Codex executable itself was missing.
- This is benchmark Q1, so no Python standard-library runtime documentation was consulted.

### Anonymous answer assessments

| Repeat | Label | Verdict | Correct | False | Unsupported | Dependencies found / total | Critical dependencies missed | Unsupported edges |
|---|---|---|---:|---:|---:|---:|---|---:|
| R1 | X | partial | 8 | 1 | 0 | 8 / 9 | D8 | 0 |
| R1 | Y | partial | 9 | 1 | 0 | 6 / 9 | D6, D7, D8 | 0 |
| R2 | X | partial | 9 | 0 | 0 | 8 / 9 | D8 | 0 |
| R2 | Y | partial | 9 | 1 | 1 | 6 / 9 | D6, D7, D8 | 0 |

## Q2

The source defines a conditional path, not one actual failed run. `main.main` validates the `ExecutionInput`, creates `OrchestratorState`, calls `run_codex`, validates its result, assigns `last_execution` and appends it to history, then calls and validates `route_decision` before saving and applying the route (`main.py:main:21-45`). Input validation requires PASS, readiness, valid DSL structure, a workspace root, and in-range policy limits; it does not require DSL_READY (`contracts.py:validate_execution_input:200-228`). `run_codex` writes a temporary spec, builds a command, calls `subprocess.run`, and constructs an `ExecutionResult` for returned processes, timeouts, and FileNotFoundError; its `finally` attempts temporary-file cleanup (`codex_run.py:run_codex:36-123`). The router handles success first; for failures it checks DSL blockers, then stuck-loop status, then error type (`routing_system.py:route_decision:33-118`). Route application updates retry or repair counters in `main`; a repair hook is explicitly unimplemented. Exit status, output text, exceptions, input DSL, prior history, and policy determine the concrete route at runtime.

### Required dependencies
- **D1** (critical): `contracts.py::ExecutionInput; validate_execution_input` — The input contract and gate used by main before entering the execution loop. Evidence: contracts.py:ExecutionInput:79-84; contracts.py:validate_execution_input:200-228; main.py:main:21-24
- **D2** (critical): `codex_run.py::run_codex` — The direct call from the orchestrator into the execution adapter, passing the input and state. Evidence: main.py:main:36; codex_run.py:run_codex:22-46
- **D3** (critical): `contracts.py::ExecutionResult; TestResult` — The adapter constructs the result contract for a returned process, timeout, or missing command; it does not itself update orchestrator state. Evidence: codex_run.py:run_codex:53-75; codex_run.py:run_codex:77-119; contracts.py:ExecutionResult:95-104; contracts.py:TestResult:88-93
- **D4** (critical): `contracts.py::validate_execution_result` — The result contract gate called before the result is stored or routed. Evidence: main.py:_validate_or_stop_result:79-83; contracts.py:validate_execution_result:231-249
- **D5** (critical): `contracts.py::OrchestratorState` — The state contract holds counters, last result and route, current DSL, and execution history; main appends the result before routing. Evidence: contracts.py:OrchestratorState:118-128; main.py:main:26-27; main.py:main:39-42
- **D6** (critical): `routing_system.py::route_decision` — The orchestrator passes the result, updated state/history, and input to the router to select a route. Evidence: main.py:main:42; routing_system.py:route_decision:19-23
- **D7** (critical): `contracts.py::RouteDecision; can_retry_codex; can_repair_spec; contains_blocking_marker; is_none_section` — The router returns the route contract and calls contract helpers for blocker checks and retry/repair eligibility. Evidence: routing_system.py:route_decision:33-118; routing_system.py:_dsl_has_blocking_state:121-139; routing_system.py:_repair_or_regenerate:174-195; routing_system.py:_repair_or_fail:198-219; contracts.py:can_retry_codex:270-274; contracts.py:can_repair_spec:277-281
- **D8** (critical): `contracts.py::validate_route_decision` — The route contract gate called by main before recording and applying the route. Evidence: main.py:_validate_or_stop_decision:85-88; contracts.py:validate_route_decision:252-267
- **D9** (critical): `main.py::_apply_retry_code_route; _apply_repair_spec_route` — Application-time budget checks and counter updates; exhausted application-time budgets set total_cycles to the maximum. Evidence: main.py:_apply_retry_code_route:91-99; main.py:_apply_repair_spec_route:102-111; contracts.py:can_retry_codex:270-274; contracts.py:can_repair_spec:277-281

### Tests and runtime notes

The tracked tree contains no test files or test directory. The Python-source search found no checked-in caller or test consumer for `main`; its direct-execution branch exits with instructions to build an ExecutionInput and call main (`main.py:118-122`). No checked-in tests or executable consumer are available to confirm runtime behavior. This does not rule out consumers outside the supplied worktree.
- No concrete ExecutionInput, subprocess result, output, or exception is supplied; therefore the actual error type, route, and terminal outcome cannot be selected from source alone.
- For returned subprocesses, the adapter branches on returncode and classifies nonzero output using ordered substring checks. Actual output and returncode are runtime values.
- The adapter catches TimeoutExpired and FileNotFoundError; other exceptions are not converted into ExecutionResult by the shown code.
- The router evaluates the DSL and current history, including the current result already appended by main. Its test signal is not used as a routing condition.

### Anonymous answer assessments

| Repeat | Label | Verdict | Correct | False | Unsupported | Dependencies found / total | Critical dependencies missed | Unsupported edges |
|---|---|---|---:|---:|---:|---:|---|---:|
| R1 | X | partial | 7 | 1 | 1 | 7 / 9 | D4, D8 | 0 |
| R1 | Y | partial | 5 | 1 | 1 | 8 / 9 | D8 | 1 |
| R2 | X | partial | 6 | 1 | 2 | 8 / 9 | D8 | 1 |
| R2 | Y | partial | 5 | 1 | 2 | 8 / 9 | D8 | 1 |

## Q3

At HEAD 37bc219ae4f5989d0bfaf6bfb917ae86108d33e1, the tracked tree contains four Python files and three Markdown files; git status is clean. contracts.py:ExecutionErrorType:11-19 declares the current Literal values. ExecutionResult.error_type and RouteDecision.source_error_type use it, and OrchestratorState stores ExecutionResult objects in last_execution and history (contracts.py:95-128). validate_execution_result checks status/error consistency, exit code, and test-result consistency, but has no allowed-value membership check; validate_route_decision likewise does not check source_error_type membership (contracts.py:231-267). codex_run.py:run_codex:22-119 assigns NONE on success, calls classify_error for nonzero subprocess exits, and assigns CODEX_ERROR or ENV_ERROR in timeout and missing-command handlers. classify_error uses ordered text checks and returns only existing categories or UNKNOWN (codex_run.py:180-211). _build_summary interpolates the error value (codex_run.py:214-217). routing_system.py:route_decision:19-118 handles success first, then DSL blockers, stuck loops, named error categories, and finally FATAL for an unmatched category; _detect_stuck_loop and _route_stuck_loop compare repeated categories and send unlisted repeated categories to FATAL (routing_system.py:142-171). main.py:main:21-76 validates, records, routes, and acts on results. contracts.py:to_dict:131-132 uses dataclasses.asdict, with no in-repository call site. codex_run.py:_write_temp_spec:126-155 writes input DSL, validator data, and metadata, not ExecutionResult; there is no result parser or deserializer. No separate execution-error schema, tests, or documentation defining this taxonomy is tracked. Task documents discuss analysis categories and MCP/config failure as benchmark instructions; the SOP discusses generic error handling, not these error values.

### Required dependencies
- **Q3-D1** (critical): `contracts.py::ExecutionErrorType` — The Literal declaration whose allowed values are being expanded. Evidence: contracts.py:ExecutionErrorType:11-19
- **Q3-D2** (critical): `contracts.py::ExecutionResult.error_type; RouteDecision.source_error_type; OrchestratorState.last_execution/history` — Typed result, decision, and history fields through which the error value is carried. Evidence: contracts.py:ExecutionResult:95-104; contracts.py:RouteDecision:107-115; contracts.py:OrchestratorState:118-128
- **Q3-D3** (critical): `contracts.py::validate_execution_result` — Checks status/error consistency and other result invariants without enumerating allowed error values. Evidence: contracts.py:validate_execution_result:231-249
- **Q3-D4** (critical): `codex_run.py::run_codex` — Produces ExecutionResult values and selects the classifier or direct exception categories. Evidence: codex_run.py:run_codex:22-75; codex_run.py:run_codex:77-119
- **Q3-D5** (critical): `codex_run.py::classify_error` — Text classifier for nonzero process exits; it currently has no MCP-specific category. Evidence: codex_run.py:classify_error:180-211
- **Q3-D6** (critical): `routing_system.py::route_decision` — Maps status, blockers, and known error categories to routes; unmatched failed-result categories reach the FATAL fallback when earlier conditions do not apply. Evidence: routing_system.py:route_decision:19-118
- **Q3-D7** (critical): `routing_system.py::_detect_stuck_loop; _route_stuck_loop` — Detects repeated error values and routes repeated categories outside the special repair set to FATAL. Evidence: routing_system.py:_detect_stuck_loop:142-149; routing_system.py:_route_stuck_loop:152-171
- **Q3-D8** (critical): `main.py::main` — Validates and records each result, invokes routing, and carries out the selected route. Evidence: main.py:main:21-76
- **Q3-D9** (supporting): `contracts.py::validate_route_decision` — Validates route-decision confidence, reason, and route/spec-change consistency, but not source_error_type membership. Evidence: contracts.py:validate_route_decision:252-267
- **Q3-D10** (supporting): `contracts.py::to_dict` — Generic dataclass serializer that can carry the string value if called; no repository caller is present. Evidence: contracts.py:to_dict:131-132
- **Q3-D11** (supporting): `codex_run.py::_write_temp_spec` — Relevant serialization check: this writes an input spec, not an ExecutionResult serializer. Evidence: codex_run.py:_write_temp_spec:126-155
- **Q3-D12** (supporting): `codex_run.py::_build_summary` — Interpolates the error category into the failure summary. Evidence: codex_run.py:_build_summary:214-217

### Tests and runtime notes

No test files are tracked, so there are no in-repository tests to update or inspect; no tests were run. No separate execution-error schema, result parser/deserializer, or result JSON reader is present. to_dict has no in-repository call site. The only nearby JSON writer serializes the input spec, not ExecutionResult. The SOP and task documents do not define this error taxonomy.
- The checked-in classifier consumes external subprocess stdout/stderr using ordered substring checks. An MCP startup diagnostic could match one of the existing generic branches or fall through to UNKNOWN; the repository does not establish the diagnostic wording or MCP startup behavior.
- Adding the Literal value alone supplies no producer branch. An external caller could construct an ExecutionResult containing that string, but out-of-checkout callers and consumers are unknown.

### Anonymous answer assessments

| Repeat | Label | Verdict | Correct | False | Unsupported | Dependencies found / total | Critical dependencies missed | Unsupported edges |
|---|---|---|---:|---:|---:|---:|---|---:|
| R1 | X | partial | 5 | 1 | 0 | 12 / 12 | None | 0 |
| R1 | Y | partial | 5 | 0 | 1 | 11 / 12 | None | 1 |
| R2 | X | complete | 6 | 0 | 0 | 11 / 12 | None | 0 |
| R2 | Y | partial | 7 | 0 | 1 | 11 / 12 | None | 1 |

## Q4

At HEAD 37bc219ae4f5989d0bfaf6bfb917ae86108d33e1, ExecutionInput.metadata is a general dict and timeout_seconds is not a RunPolicy field (contracts.py:ExecutionInput:79-84; RunPolicy:71-75). validate_execution_input checks readiness, DSL, workspace, and policy limits, but does not validate timeout metadata (contracts.py:validate_execution_input:200-228). _timeout_seconds selects metadata['timeout_seconds'] only when isinstance(value, int) and value > 0; otherwise it returns DEFAULT_TIMEOUT_SECONDS=300 (codex_run.py:DEFAULT_TIMEOUT_SECONDS:19; _timeout_seconds:166-170). _write_temp_spec also serializes the metadata, but run_codex supplies the selected timeout directly to subprocess.run (codex_run.py:_write_temp_spec:126-155; run_codex:36-46).

If subprocess.run returns, run_codex derives status from returncode and calls classify_error only for nonzero returns (codex_run.py:run_codex:48-75). The classifier checks test, spec, validation, and environment text before timeout/runtime/exception terms (codex_run.py:classify_error:180-212). If TimeoutExpired is raised, the separate handler constructs FAILED with exit_code=-1 and error_type=CODEX_ERROR, adds available exception output to logs/raw (or a fallback stderr message), sets tests.ran=False, and records timeout_seconds by calling the helper again; it does not call classify_error (codex_run.py:run_codex:77-101). The finally block attempts temporary-spec cleanup and ignores OSError (codex_run.py:run_codex:121-123; _cleanup_temp_spec:173-177).

main validates the result, sets last_execution, appends it to history, and then calls route_decision (main.py:main:36-43). Routing prioritizes success, blocking DSL state, stuck-loop detection, and then error-type dispatch; a non-blocked, non-stuck CODEX_ERROR routes to RETRY_CODEX if can_retry_codex permits, otherwise FATAL (routing_system.py:route_decision:33-52,86-101; contracts.py:can_retry_codex:270-274). The detector takes the last STUCK_LOOP_WINDOW-1 history errors and appends the current error (routing_system.py:STUCK_LOOP_WINDOW:16; _detect_stuck_loop:142-149). Since main has already appended the current result, two consecutive matching failures in main can satisfy the three-item comparison. Repeated CODEX_ERROR routes to FATAL; only repeated test, spec-conflict, and validation errors enter the stuck-loop repair branch (routing_system.py:_route_stuck_loop:152-171). Blocking DSL state takes precedence and routes to REPAIR_SPEC (routing_system.py:route_decision:42-49).

main passes the same ExecutionInput to each run_codex invocation. Applying an accepted retry increments codex_retries and total_cycles, then continues; the retry handler does not change the input or its metadata (main.py:main:36,52-54; _apply_retry_code_route:91-100). The loop condition is total_cycles < max_total_cycles; an accepted retry or repair that reaches the limit leads to the max-cycle message after the loop, while SUCCESS and FATAL return earlier (main.py:main:29,48-76; _apply_repair_spec_route:102-112). The default policy is 10 total cycles and 2 Codex retries (contracts.py:RunPolicy:71-75).

The separate checked-in task document specifies a measured-session hard-timeout policy and transient-only retry policy (docs/tasks/DEVSOPBYAI-CODEXB-CODEGRAPH-CONTROLLED-REPO-NAV-AB-2026-10-02.md:TIMEOUT / RECOVERY POLICY:605-643); this is documentation, not the executable timeout/retry behavior above.

### Required dependencies
- **D1** (critical): `contracts.py::ExecutionInput` — Origin of timeout configuration: metadata is an arbitrary dict, separate from RunPolicy. Evidence: contracts.py:ExecutionInput:79-84; contracts.py:RunPolicy:71-75
- **D2** (critical): `codex_run.py::_timeout_seconds` — Reads timeout_seconds from ExecutionInput.metadata, applies the positive-int condition, and falls back to the 300-second default. Evidence: codex_run.py:DEFAULT_TIMEOUT_SECONDS:19; codex_run.py:_timeout_seconds:166-170
- **D3** (supporting): `codex_run.py::_write_temp_spec` — Serializes the same metadata into the temporary spec file; this is a side path, not the source of subprocess.run's timeout argument. Evidence: codex_run.py:_write_temp_spec:126-155
- **D4** (critical): `codex_run.py::run_codex` — Passes the selected timeout to subprocess.run and handles TimeoutExpired by directly constructing a failed CODEX_ERROR result. Evidence: codex_run.py:run_codex:22-101
- **D5** (critical): `codex_run.py::classify_error` — Classifies only normal nonzero subprocess returns; its ordered text checks are distinct from the TimeoutExpired handler. Evidence: codex_run.py:classify_error:180-212; run_codex:48-55,77-101
- **D6** (supporting): `contracts.py::validate_execution_input / validate_execution_result` — Shows which input fields are validated and that a failed result with exit_code=-1 is allowed by the result contract. Evidence: contracts.py:validate_execution_input:200-228; validate_execution_result:231-249
- **D7** (critical): `main.py::main` — Connects run_codex, result validation, history append, routing, retry/repair continuations, and loop exit. Evidence: main.py:main:21-76
- **D8** (critical): `routing_system.py::route_decision` — Defines routing precedence and the CODEX_ERROR retry-or-fatal branch. Evidence: routing_system.py:route_decision:19-118
- **D9** (critical): `routing_system.py::_detect_stuck_loop / _route_stuck_loop` — Defines the history window behavior and what repeated CODEX_ERROR does. Evidence: routing_system.py:STUCK_LOOP_WINDOW:16; _detect_stuck_loop:142-149; _route_stuck_loop:152-171
- **D10** (critical): `contracts.py::RunPolicy / can_retry_codex / can_repair_spec` — Provides retry, repair, and total-cycle limits used by the router and main loop. Evidence: contracts.py:RunPolicy:71-75; can_retry_codex:270-274; can_repair_spec:277-281
- **D11** (critical): `main.py::_apply_retry_code_route` — Increments retry/cycle counters and participates in the max-cycle stop path. Evidence: main.py:_apply_retry_code_route:91-100; main:29,52-54,75-76
- **D12** (supporting): `main.py::_apply_repair_spec_route` — Shows repair-route counter changes and that the repair hook is not implemented in this checked-in path. Evidence: main.py:main:56-59; _apply_repair_spec_route:102-112
- **D13** (supporting): `DEVSOPBYAI-CODEXB-CODEGRAPH-CONTROLLED-REPO-NAV-AB-2026-10-02.md::TIMEOUT / RECOVERY POLICY` — Separately documents measured-session timeout and retry requirements; it does not implement run_codex behavior. Evidence: docs/tasks/DEVSOPBYAI-CODEXB-CODEGRAPH-CONTROLLED-REPO-NAV-AB-2026-10-02.md:605-643

### Tests and runtime notes

The tracked tree contains no test files or test directory. Search of the checked-out source finds main.main as the sole checked-in caller of run_codex and route_decision; no other code consumer or test consumer is present. No tests were run, as instructed.
- The checked-in code establishes only that a timeout value is passed to subprocess.run and that the TimeoutExpired branch runs if that exception is raised. No timeout precision, child termination, descendant termination, or process-group behavior was verified.
- No Python standard-library documentation was inspected. Runtime-specific subprocess behavior is therefore left unasserted; the repository source itself contains no explicit process termination call.

### Anonymous answer assessments

| Repeat | Label | Verdict | Correct | False | Unsupported | Dependencies found / total | Critical dependencies missed | Unsupported edges |
|---|---|---|---:|---:|---:|---:|---|---:|
| R1 | X | partial | 8 | 0 | 1 | 10 / 13 | None | 1 |
| R1 | Y | partial | 7 | 0 | 1 | 11 / 13 | None | 0 |
| R2 | X | complete | 10 | 0 | 1 | 11 / 13 | None | 0 |
| R2 | Y | partial | 10 | 0 | 2 | 11 / 13 | None | 1 |

## Paired safety finding

Safety Gate: **FAIL**. The Q1/R2 B answer omitted critical dependencies D6 and D7 (`can_retry_codex`, `can_repair_spec` in `main.py` and `routing_system.py`) that the paired Q1/R2 A answer found; both missed D8. The Q1/R1 result reversed this pattern: A missed D6/D7 while B found them. This is a run-level regression with substantial repeat variation. It still fails the task safety gate because the gate is triggered by any new critical dependency miss.

No validator identified an unsupported static relationship presented as confirmed runtime truth. Q4 answers separated source control flow from Python runtime behavior; the local subprocess docstring was used as runtime evidence.

### Q1 validation limitations
- Conclusions are limited to the supplied detached worktree at the specified commit; an external caller or upstream pipeline outside this checkout cannot be established.
- The tracked tree has no test files, so no test-based corroboration is available.

### Q2 validation limitations
- Validation was limited to the detached repository at the stated commit and its tracked source; no tests or runtime executions were performed.
- The absence of checked-in callers or tests does not establish that no external consumer exists.

### Q3 validation limitations
- The specified HEAD was verified and the working tree was clean. Only this detached repository worktree was inspected.
- No tests or runtime commands were run, as instructed. No external graph output or source was used to establish ground truth.

### Q4 validation limitations
- No tests were run, as instructed; the tracked tree contains no test files.
- Claims about prior answer authors' test activity or discovery provenance cannot be verified from this repository.
- The task document's measured-session TIMEOUT and transient-only retry rules are documented requirements, not evidence that the executable flow implements them.
