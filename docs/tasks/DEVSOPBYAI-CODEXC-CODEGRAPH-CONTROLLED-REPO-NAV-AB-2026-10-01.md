# TASK — DevSopByAi CodeGraph Controlled Repository-Navigation A/B Benchmark

## METADATA

- TASK_ID: DEVSOP-CODEXC-CODEGRAPH-AB-2026-10-01
- CONTRACT_VERSION: 1.0
- STATUS: READY
- IDENTITY: CodexC — Experiment Operator / Benchmark Orchestrator
- TASK_PATH: docs/tasks/DEVSOPBYAI-CODEXC-CODEGRAPH-CONTROLLED-REPO-NAV-AB-2026-10-01.md
- TASK_DEFINITION_BASE_HEAD: d51707594fff031cd54eace025b2b2ffff883f85
- TARGET: DevSopByAi working tree containing this TaskContract
- TASK_CLASS: Controlled read-only repository-navigation benchmark
- ESTIMATED_RUNTIME: 90–150 minutes typical
- EXECUTION_MODE: unattended-capable; serial orchestration of fresh child Codex sessions
- CONTRACT_IMMUTABILITY: Do not rewrite this contract, benchmark count, arm definitions, acceptance criteria, or failure policy during execution.

## GOAL

Determine whether CodeGraph improves Codex repository discovery on the current DevSopByAi repository without reducing correctness or dependency coverage.

The experiment must answer:

On the same frozen repository HEAD, with identical benchmark prompts, identical Codex model/reasoning, and fresh isolated contexts, does CodeGraph reduce repository-exploration cost while preserving correctness and dependency completeness?

Priority order:

1. correctness failures;
2. dependency recall and critical omissions;
3. tool calls;
4. unique files opened;
5. total tokens where observable;
6. wall-clock time.

Correctness is the gate. Efficiency is considered only after correctness.

## CODEXC ROLE

CodexC is the experiment operator, not the benchmark subject.

CodexC must:

- freeze the repository and benchmark environment;
- choose and freeze benchmark prompts before any measured answer session;
- launch a fresh child Codex CLI process/session for every measured run;
- collect machine-readable evidence;
- launch fresh independent blinded validator session(s);
- write the final report only after validation.

CodexC must not answer a benchmark itself and then reuse that knowledge in a measured child session.

## MODEL INVARIANTS

For every measured Arm A and Arm B child session:

- exact same model;
- exact same reasoning/effort setting;
- exact same frozen benchmark prompt;
- exact same BENCHMARK_HEAD;
- same timeout policy;
- same baseline instructions except the minimum CodeGraph-specific discovery instruction required for Arm B.

Record exact model, reasoning setting, Codex version and environment in manifest.json. If any value cannot be observed reliably, record UNKNOWN; never guess.

## PRECONDITIONS

Before measurement:

1. Confirm this TaskContract is present locally.
2. Record git rev-parse HEAD, git status --porcelain, git remote -v, and current branch/ref.
3. Require a clean working tree before benchmark setup.
4. Define BENCHMARK_HEAD as the exact commit under test after this TaskContract is available locally.
5. Verify Codex CLI can launch fresh non-resumed child sessions.
6. Inspect current CodeGraph installation/configuration behavior before making environment changes.
7. Do not modify DevSopByAi source, tests, schemas, AGENTS instructions, or production configuration during the measured benchmark.

If the current working tree is not a usable DevSopByAi repository, is unexpectedly dirty, or fresh child contexts cannot be isolated, stop as BLOCKED.

## ARM A — BASELINE

CodeGraph must not be available.

Allowed read-only discovery includes source reads, rg/grep, find, Git inspection, and existing repository-native read-only tools.

No source modification. No implementation patch.

## ARM B — CODEGRAPH

CodeGraph is enabled as an MCP/discovery layer.

Use CodeGraph-first discovery, but allow source reads, rg, Git, tests, and other read-only confirmation when needed to verify:

- critical dependency edges;
- dynamic/runtime-only behavior;
- macro/framework/plugin behavior;
- uncertain CodeGraph results.

Do not instruct the child agent to trust CodeGraph blindly.

No source modification. No implementation patch.

The comparison is normal Codex exploration versus Codex with CodeGraph available as a preferred discovery layer. It is not a CodeGraph-only versus grep-only contest.

## CODEGRAPH ISOLATION RULES

Do not run a global installer blindly.

Preflight should inspect current official/current command behavior, including codegraph version/help/install help where applicable.

Requirements:

- do not modify repository AGENTS.md or equivalent instruction files;
- do not modify persistent/global Codex instructions;
- do not commit .codegraph;
- do not modify production DevSopByAi config;
- prefer a documented temporary/per-run MCP configuration;
- disable telemetry for the experiment where supported;
- do not copy/expose credentials merely to manufacture an isolated HOME;
- if safe per-run isolation cannot be achieved without persistent/global mutation, mark Arm B BLOCKED rather than mutating the global environment.

Record exact CodeGraph version, installation source/method, index command, index wall time, index result, and index size if observable.

## BENCHMARK DESIGN

Phase 1 is read-only repository understanding. Do not use real implementation/patch tasks.

Freeze exactly four prompts in docs/experiments/codegraph-ab-2026-10/benchmark-prompts.json before the first measured session.

### Q1 — Entry Point Discovery

Choose one real core behavior. Ask for the path from a public/CLI/API entry point to the effective executor/handler, including relevant dispatcher/router, loader/parser, executor/handler, result/evidence writer, and important branches where present.

### Q2 — Cross-file Call Chain

Choose one real multi-file core behavior such as TaskContract/execution/state/evidence flow. Ask for the complete cross-file call/data path, files and symbols, role of every hop, and distinction between confirmed calls and inferred relationships.

### Q3 — Blast Radius

Choose one real schema/contract/state/evidence field or symbol. Pose a hypothetical read-only change-impact question. Require direct consumers, indirect consumers, tests, parser/serializer/schema users, runtime/validator users, and uncertain/runtime-only dependencies.

### Q4 — Dynamic / Recovery Path

Choose one real behavior likely to exercise static-analysis limits, preferably involving subprocess, config-driven dispatch, dynamic import, runtime branching, plugin/extension selection, shell, Git/runtime state, recovery, or unexpected-state handling.

Ask for the end-to-end path and require explicit uncertainty where static evidence is insufficient.

Benchmark constraints:

- prompts must be frozen before measured execution;
- prompts must not reveal expected answers;
- prompts may not change after the first measured session;
- do not choose four trivial single-file questions;
- Q2 and Q3 must require multiple files/symbol relationships;
- Q4 must intentionally probe a plausible static-analysis weakness.

## RUN MATRIX

Run 4 prompts × 2 repetitions × 2 arms = 16 measured subject sessions.

Every measured session must be:

- a fresh Codex process/session;
- fresh conversational context;
- pinned to BENCHMARK_HEAD;
- same prompt/model/reasoning for corresponding A/B runs;
- subject to the same timeout.

No answer or context from one run may be inserted into another.

Balance order to reduce simple warm-cache bias:

- Q1 R1: A then B
- Q1 R2: B then A
- Q2 R1: B then A
- Q2 R2: A then B
- Q3 R1: A then B
- Q3 R2: B then A
- Q4 R1: B then A
- Q4 R2: A then B

Record actual order and any deviation.

## WORKTREE AND MUTATION CONTROL

Use disposable worktrees or equivalent clean snapshots pinned to BENCHMARK_HEAD.

For every measured session:

1. check clean state before launch;
2. run read-only benchmark;
3. check git status --porcelain after completion;
4. if the child changed repository content, preserve evidence, mark the run PROTOCOL_VIOLATION, and restore only the disposable worktree before proceeding.

The formal repository under test must receive zero unintended benchmark-time mutation.

Only final experiment artifacts required by this contract may be committed after measurement and validation.

## PER-RUN EVIDENCE

Create one JSON record per measured run with these fields:

- run_id
- benchmark_id: Q1/Q2/Q3/Q4
- arm: A/B
- repeat: 1/2
- benchmark_head
- model
- reasoning
- start_time
- end_time
- wall_seconds
- tool_calls_total
- search_calls
- grep_calls
- read_calls
- codegraph_calls
- unique_files_read
- unique_files_referenced
- input_tokens
- output_tokens
- cached_tokens
- total_tokens
- retrieval_bytes
- retrieval_tokens
- answer_file
- status: COMPLETE/TIMEOUT/ERROR/PROTOCOL_VIOLATION
- timeout
- blocked
- errors

If a metric is not observable, store null. Never estimate unavailable token/tool metrics.

Do not commit secrets, auth material, or oversized raw traces.

## RETRIEVAL FOOTPRINT

Where observable, measure both:

- files explicitly opened/read;
- context returned by tools in bytes and/or tokens.

Fewer tool calls alone is not sufficient evidence of lower context cost.

If footprint cannot be measured reliably, record null and describe the limitation.

## SETUP COST AND BREAK-EVEN

Measure CodeGraph setup separately.

Record:

- T_setup: first index/setup wall time;
- T_query: measured query/session time;
- T_first_use: T_setup plus first CodeGraph query/session cost.

If median per-task wall-time saving is positive, compute a descriptive break-even estimate:

break_even_tasks = T_setup / median_wall_time_saved_per_task

If the denominator is zero/negative or data is insufficient, report N/A.

Report both first-use and steady-state views.

## INDEPENDENT BLINDED VALIDATION

After subject runs complete, launch fresh validator session(s).

The validator must not be told which anonymous answer came from Arm A or B.

Create X/Y anonymous labels and keep the arm mapping outside the validator prompt until validation is complete.

Validator ground truth must come from repository source, Git, tests, and read-only runtime evidence as appropriate.

CodeGraph must not be the sole ground truth for validating CodeGraph.

Validate at least:

- cited file exists;
- cited symbol exists;
- claimed call/data relation is supported;
- direct dependencies are not omitted;
- invented edges are identified;
- static hypotheses are not mislabeled as runtime truth;
- runtime/dynamic uncertainty is recognized.

Prefer one fresh validator context per Q1–Q4 where practical.

## VALIDATION METRICS

Do not use vague 1–10 scores as the primary evidence.

For each answer/run record:

- correct factual claims;
- false factual claims;
- required dependencies found;
- required dependencies missed;
- critical omission count;
- unsupported edge count.

Where defensible:

dependency_recall = confirmed_required_dependencies_found / all_validator_confirmed_required_dependencies

claim_precision = correct_claims / (correct_claims + false_claims)

If the denominator cannot be defended, report N/A rather than inventing a score.

## DECISION GATES

### Safety Gate

Arm B must not introduce:

- a new critical correctness failure;
- a missed validator-confirmed critical dependency attributable to CodeGraph use;
- an unsupported static relation presented as confirmed runtime truth.

Any such event must be prominent in the report and prevents unqualified adoption.

### Utility Gate

Only after Safety Gate evaluation compare:

- tool calls;
- unique files opened;
- wall time;
- total tokens;
- retrieval footprint.

Use medians as primary summaries. Means may be supplemental. Do not call improvement stable if one extreme benchmark drives the aggregate.

## FAILURE-CASE REPORT

Create docs/experiments/codegraph-ab-2026-10/validation/CODEGRAPH_FAILURE_CASES.md.

Track observed:

- missing edge;
- wrong/stale edge;
- dynamic-dispatch miss;
- macro/framework miss;
- runtime-only path;
- retrieval bloat;
- MCP/config failure;
- installation/index failure.

If none is observed, explicitly write: No observed failure case in this benchmark.

## TIMEOUT / RECOVERY POLICY

Measured subject session:

- soft limit 8 minutes;
- hard limit 12 minutes.

On hard timeout: terminate, record TIMEOUT, continue.

CodeGraph setup/index hard limit: 20 minutes.

If exceeded: preserve diagnostics, mark Arm B PARTIAL/BLOCKED as appropriate, and continue only with work that remains meaningful.

At most one retry is allowed, and only for a clearly transient infrastructure failure such as process startup or temporary transport failure.

Do not retry because an answer was wrong, CodeGraph returned poor/empty results, logical analysis failed, genuine workload timed out, or a protocol violation occurred.

Record every retry.

## REQUIRED OUTPUT TREE

Create under docs/experiments/codegraph-ab-2026-10:

- README.md
- manifest.json
- benchmark-prompts.json
- arm-map.json
- runs/
- answers/
- validation/ground-truth.md
- validation/validation.json
- validation/CODEGRAPH_FAILURE_CASES.md
- metrics.csv
- FINAL-REPORT.md

Do not expose arm-map.json to validator sessions before validation is complete.

## ACCEPTANCE CRITERIA

- AC-01: BENCHMARK_HEAD, environment, Codex version, model, reasoning, and CodeGraph version recorded.
- AC-02: pre/post clean-state evidence exists.
- AC-03: Q1–Q4 prompts frozen before measured execution and unchanged afterward.
- AC-04: 16 measured subject-session records exist, including timeout/error records where applicable.
- AC-05: every measured run used a fresh child Codex context/process.
- AC-06: corresponding A/B runs used the same HEAD, prompt, model, reasoning, and timeout.
- AC-07: Arm A had no CodeGraph access.
- AC-08: Arm B used isolated CodeGraph integration without persistent/global instruction pollution.
- AC-09: CodeGraph setup/index time recorded separately.
- AC-10: no measured child silently modified repository state.
- AC-11: blinded independent validation performed without using CodeGraph as sole ground truth.
- AC-12: correctness/dependency results reported before efficiency conclusions.
- AC-13: medians for tool calls, files opened, wall time, and tokens reported where observable; unavailable metrics explicitly null/N/A.
- AC-14: CODEGRAPH_FAILURE_CASES.md exists.
- AC-15: FINAL-REPORT.md states limitations and protocol deviations.
- AC-16: experiment artifacts committed; .codegraph is not committed.
- AC-17: formal DevSopByAi source/runtime behavior was not changed by this Phase-1 task.

If a structural precondition prevents fair comparison, return BLOCKED rather than weakening the contract.

## FORBIDDEN ACTIONS

Do not:

- modify this TaskContract during execution;
- change benchmark prompts after measured execution starts;
- reuse conversational context across measured runs;
- leak A answers into B prompts or vice versa;
- ban source verification in Arm B merely to make CodeGraph metrics look better;
- globally rewrite Codex/MCP/AGENTS config for convenience;
- commit .codegraph;
- modify production source/tests;
- run a Phase-2 implementation benchmark here;
- rerun incorrect answers until they pass;
- fabricate unavailable metrics;
- use CodeGraph to validate itself;
- hide setup/index cost;
- delete evidence of failure or protocol violation.

## UNEXPECTED STATE POLICY

On unexpected state:

1. preserve evidence;
2. do not silently change the contract;
3. classify as transient infrastructure, environment incompatibility, benchmark-design invalidity, CodeGraph limitation, Codex limitation, or protocol violation;
4. continue only if fairness is preserved;
5. otherwise stop as PARTIAL or BLOCKED.

If current CodeGraph/Codex CLI behavior differs from assumptions, use current documented behavior while preserving these invariants:

same HEAD; same prompt; fresh context; isolation; no unintended repository mutation; blinded independent validation.

## FINAL REPORT SCHEMA

FINAL-REPORT.md must include:

- TASK_ID / CONTRACT_VERSION / STATUS: COMPLETE, PARTIAL, or BLOCKED
- BENCHMARK_HEAD / FINAL_COMMIT / CHANGED_FILES
- CODEX_VERSION / MODEL / REASONING
- CODEGRAPH_VERSION / CODEGRAPH_SETUP_SECONDS
- benchmark matrix and completed/timeout/error/protocol-violation counts
- correctness summary
- dependency recall
- critical omissions
- unsupported edges
- median tool calls
- median unique files opened
- median wall seconds
- median total tokens
- retrieval footprint
- first-use view
- steady-state view
- break-even tasks
- CodeGraph failure modes
- limitations
- protocol deviations
- AC-01 through AC-17 as PASS/FAIL/N/A
- ENGINEERING_DISPOSITION
- DISPOSITION_BASIS

ENGINEERING_DISPOSITION must be exactly one of:

- ADOPT
- ADOPT_WITH_GUARDRAILS
- DO_NOT_ADOPT
- INCONCLUSIVE

Disposition definitions:

- ADOPT: Safety Gate passes and utility improvement is consistent enough to justify default discovery use.
- ADOPT_WITH_GUARDRAILS: useful improvement exists, but source/runtime revalidation is required for critical paths or observed static-analysis gaps.
- DO_NOT_ADOPT: material correctness regression, critical dependency loss, unacceptable operational cost, or no useful benefit.
- INCONCLUSIVE: evidence is insufficient or the protocol could not be completed fairly.

## PHASE BOUNDARY

This task is Phase 1 only: repository navigation and understanding.

Do not perform real implementation patches.

A future Phase 2 may separately test real patch generation, tests, time-to-first-correct-patch, regression, touched files, and ExecutionEvidence.
