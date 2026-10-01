# TASK CONTRACT — DevSopByAi CodeGraph Controlled Repository-Navigation A/B Benchmark

## METADATA

- TASK_ID: DEVSOP-CODEXC-CODEGRAPH-AB-2026-10-01
- TASK_NAME: DevSopByAi CodeGraph Controlled Repository-Navigation A/B Benchmark
- CONTRACT_VERSION: 2.0
- STATUS: READY
- ASSIGNEE_IDENTITY: CodexC
- ASSIGNEE_ROLE: Experiment Operator / Benchmark Orchestrator
- TASK_PATH: docs/tasks/DEVSOPBYAI-CODEXC-CODEGRAPH-CONTROLLED-REPO-NAV-AB-2026-10-01.md
- CREATED_FROM_HEAD: 9f5d1701854428a3ee0f20c6eff8021f139abdd0
- TARGET_REPOSITORY: the DevSopByAi working tree in which this TaskContract is present
- TASK_CLASS: controlled read-only repository-navigation benchmark
- CONTRACT_IMMUTABLE: true
- PHASE: 1 — repository understanding / navigation only

This file is the Layer-B TaskContract and is the sole execution authority for CodexC.
Chat text and launch prompts are only locators. If chat text conflicts with this file, this file wins.

## EXECUTION PROFILE

- OPERATOR: CodexC
- OPERATOR_MODE: orchestrator, not benchmark subject
- RECOMMENDED_REASONING: high
- EXPECTED_RUNTIME: 90–150 minutes typical
- UNATTENDED_EXECUTION: allowed
- MEASURED_SUBJECT_SESSIONS: 16
- BENCHMARK_COUNT: 4
- REPEATS_PER_BENCHMARK: 2
- ARMS: A = baseline Codex navigation; B = CodeGraph-assisted Codex navigation
- VALIDATION: independent and blinded
- SOURCE_MUTATION_DURING_MEASUREMENT: forbidden
- PHASE_2_PATCHING: out of scope

For all measured Arm-A and Arm-B child sessions, use the exact same Codex model, reasoning/effort setting, frozen benchmark prompt, BENCHMARK_HEAD, timeout policy, and baseline instructions, except for the minimum CodeGraph availability/discovery instruction required for Arm B.

If exact model or metric identity cannot be observed, record UNKNOWN or null. Never guess.

## GOAL

Determine whether CodeGraph is useful as a default repository-discovery layer for Codex on the current DevSopByAi repository.

The experiment must answer:

> On the same frozen repository HEAD, with identical benchmark prompts and fresh isolated Codex contexts, does CodeGraph reduce repository-exploration cost without reducing correctness or dependency completeness?

Decision order is fixed:

1. correctness;
2. critical dependency completeness;
3. unsupported/static-vs-runtime claims;
4. tool calls;
5. unique files opened;
6. token use where observable;
7. wall-clock time;
8. CodeGraph setup/index cost.

Correctness is a gate. Efficiency cannot compensate for a correctness regression.

## PRECONDITIONS

Before any measured run, CodexC MUST:

1. Read this TaskContract in full.
2. Confirm the current working tree is the intended DevSopByAi repository.
3. Record:
   - git rev-parse HEAD
   - git status --porcelain
   - git branch --show-current or equivalent detached-ref evidence
   - git remote -v
   - Codex CLI version
4. Require the working tree to be clean before benchmark setup.
5. Define BENCHMARK_HEAD as the exact commit under test after this TaskContract is present locally.
6. Verify fresh non-resumed child Codex sessions can be launched.
7. Verify the measured repository has enough real cross-file structure to support all four benchmark categories below.
8. Inspect current CodeGraph documentation/help/configuration behavior before changing any environment.
9. Confirm CodeGraph can be isolated from persistent/global Codex/AGENTS configuration.
10. Create a dedicated experiment output root:
    docs/experiments/codegraph-ab-2026-10/

BLOCK before measurement if any of the following is true:

- this TaskContract cannot be read;
- the wrong repository is open;
- the working tree is unexpectedly dirty and cannot be safely explained;
- fresh child Codex contexts cannot be isolated;
- the repository is too structurally trivial to form four valid benchmarks;
- safe CodeGraph isolation cannot be achieved without persistent/global mutation.

Do not weaken the experiment to avoid BLOCKED status.

## EXACT EXECUTION PLAN

### Phase 0 — Freeze execution state

Create manifest.json containing at minimum:

- TASK_ID
- CONTRACT_VERSION
- BENCHMARK_HEAD
- repository path
- branch/ref
- initial git status
- Codex version
- measured Codex model
- reasoning/effort setting
- host/OS summary
- CodeGraph version once known
- planned run matrix
- start timestamp

After BENCHMARK_HEAD is frozen, every measured child session MUST operate on that same commit via disposable clean worktree/snapshot.

### Phase 1 — Inspect and isolate CodeGraph

Inspect current CodeGraph CLI/help/documentation and establish the least-invasive integration method.

Requirements:

- do not run a global installer blindly;
- do not edit repository AGENTS.md or equivalent instruction files;
- do not edit persistent/global Codex instructions;
- do not change production DevSopByAi configuration;
- do not commit .codegraph;
- prefer temporary/per-run MCP configuration or another documented isolated method;
- disable telemetry where supported;
- do not copy credentials/tokens into temporary homes merely to make the test work.

Record:

- exact CodeGraph version;
- install/source method;
- configuration method;
- index command;
- index start/end time;
- setup/index wall time;
- setup/index status;
- index size if observable.

CodeGraph setup/index has its own timing and MUST NOT be silently folded into per-query latency.

### Phase 2 — Build and freeze the benchmark set

CodexC may inspect source/docs/tests only to choose benchmark targets.

Freeze exactly four prompts in:

docs/experiments/codegraph-ab-2026-10/benchmark-prompts.json

The four categories are mandatory:

#### Q1 — Entry Point Discovery

Choose one real core behavior and ask for the complete path from a public/CLI/API entry point to the effective executor/handler.

Expected answer dimensions, where present:

- entry point;
- dispatcher/router;
- loader/parser;
- executor/handler;
- result/evidence writer;
- important condition branches.

#### Q2 — Cross-file Call/Data Chain

Choose one real multi-file core behavior such as contract → execution → state → evidence.

Require:

- files;
- symbols;
- complete cross-file path;
- role of each hop;
- confirmed relations separated from inferred relations.

#### Q3 — Blast Radius

Choose one real schema/contract/state/evidence field or symbol and pose a hypothetical read-only change-impact question.

Require:

- direct consumers;
- indirect consumers;
- parser/serializer/schema consumers;
- runtime/validator consumers;
- relevant tests;
- uncertain or runtime-only dependencies.

No actual modification is allowed.

#### Q4 — Dynamic / Recovery / Runtime-selected Path

Choose one real behavior that plausibly stresses static analysis, preferably involving one or more of:

- subprocess;
- runtime branching;
- config-driven dispatch;
- dynamic import;
- plugin/extension selection;
- shell;
- Git/runtime state;
- recovery or unexpected-state handling.

Require an end-to-end explanation and explicit uncertainty wherever static evidence is insufficient.

Benchmark-selection invariants:

- all four prompts are frozen before the first measured session;
- prompts do not contain expected answers;
- prompts do not change after measurement starts;
- do not choose four trivial single-file questions;
- Q2 and Q3 must require multiple files/symbol relationships;
- Q4 must intentionally probe a plausible static-analysis weakness.

After benchmark-prompts.json is frozen, compute and record its checksum in manifest.json.

### Phase 3 — Prepare the two arms

#### Arm A — BASELINE

CodeGraph MUST NOT be available to the child session.

Allowed read-only navigation:

- source reads;
- rg/grep;
- find;
- Git inspection;
- existing repository-native read-only tools.

No source modifications. No implementation patch.

#### Arm B — CODEGRAPH

CodeGraph is available as a preferred discovery layer.

Instruction policy:

- use CodeGraph-first discovery;
- source/rg/Git/tests/read-only runtime verification remain allowed;
- critical edges, dynamic behavior, macros/framework magic, plugins, and uncertain results SHOULD be verified from source/runtime evidence;
- never instruct the subject to trust CodeGraph blindly.

No source modifications. No implementation patch.

This experiment compares normal Codex navigation against Codex with CodeGraph available. It does NOT compare “CodeGraph only” against “grep only”.

### Phase 4 — Execute the measured run matrix

Run exactly:

4 benchmarks × 2 repetitions × 2 arms = 16 measured subject sessions.

Every measured run MUST use:

- a fresh Codex process/session;
- no resumed conversation;
- the same BENCHMARK_HEAD;
- the same prompt for matching A/B pairs;
- the same model/reasoning;
- the same timeout limits.

No measured answer may be copied into another measured prompt/context.

Use this deterministic balanced order unless a recorded infrastructure constraint makes it impossible:

- Q1 R1: A → B
- Q1 R2: B → A
- Q2 R1: B → A
- Q2 R2: A → B
- Q3 R1: A → B
- Q3 R2: B → A
- Q4 R1: B → A
- Q4 R2: A → B

Record the actual order.

For every measured run:

1. create/reset disposable worktree/snapshot at BENCHMARK_HEAD;
2. verify clean state before launch;
3. launch a fresh child Codex session;
4. capture answer and observable run telemetry;
5. verify git status after completion;
6. if repository content changed, preserve evidence and mark PROTOCOL_VIOLATION;
7. restore only the disposable worktree before continuing.

Do not silently “fix” or normalize a violating run.

### Phase 5 — Capture per-run evidence

Create one JSON record per measured run containing:

- run_id
- benchmark_id
- arm
- repeat
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
- status: COMPLETE | TIMEOUT | ERROR | PROTOCOL_VIOLATION
- timeout
- blocked
- errors

If a metric is unavailable, store null. Never infer or estimate it.

Preserve only sanitized evidence in Git. Never commit secrets, tokens, auth files, or unnecessary oversized raw traces.

### Phase 6 — Measure CodeGraph setup and break-even

Report separately:

- T_setup = CodeGraph install/config/index preparation wall time;
- T_query = measured subject query/session time;
- T_first_use = T_setup + first CodeGraph-use session cost.

If median per-task wall-time saving is positive:

break_even_tasks = T_setup / median_wall_time_saved_per_task

If the denominator is zero/negative or evidence is insufficient, report N/A.

Report both first-use and steady-state views.

### Phase 7 — Blind independent validation

After all subject runs are complete:

1. anonymize corresponding A/B answers as X/Y;
2. store the arm mapping in arm-map.json;
3. do NOT expose arm-map.json to validator sessions;
4. launch fresh independent validator context(s), preferably one per benchmark Q1–Q4;
5. validators establish ground truth from source, Git, tests, and read-only runtime evidence where appropriate;
6. CodeGraph output MUST NOT be the sole ground truth for validating CodeGraph.

Validators must check at minimum:

- cited file exists;
- cited symbol exists;
- claimed call/data relation is supported;
- direct dependencies are not omitted;
- invented/unsupported edges are identified;
- static hypotheses are not presented as runtime truth;
- runtime/dynamic uncertainty is recognized.

After validation is finalized, reveal the arm mapping only for metric aggregation.

### Phase 8 — Aggregate metrics

Primary correctness fields per answer:

- correct factual claims;
- false factual claims;
- required dependencies found;
- required dependencies missed;
- critical omission count;
- unsupported edge count.

Where defensible:

dependency_recall = confirmed_required_dependencies_found / all_validator_confirmed_required_dependencies

claim_precision = correct_claims / (correct_claims + false_claims)

If denominators are not defensible, report N/A.

Efficiency summary MUST use medians as the primary statistic for:

- tool calls;
- unique files opened;
- wall time;
- total tokens;
- retrieval footprint where observable.

Means may be supplemental.

Do not claim stable improvement if one extreme benchmark drives the aggregate.

### Phase 9 — Record CodeGraph failure cases

Create:

docs/experiments/codegraph-ab-2026-10/validation/CODEGRAPH_FAILURE_CASES.md

Explicitly track observed:

- missing edge;
- wrong edge;
- stale index/edge;
- dynamic-dispatch miss;
- macro/framework miss;
- runtime-only path;
- retrieval bloat;
- MCP/config failure;
- install/index failure.

If none is observed, explicitly write:

No observed failure case in this benchmark.

### Phase 10 — Apply decision gates

#### Safety Gate

Arm B fails the Safety Gate if it introduces any of:

- a new critical correctness failure;
- a missed validator-confirmed critical dependency attributable to CodeGraph-assisted navigation;
- an unsupported static relationship presented as confirmed runtime truth.

Safety Gate failure prevents unqualified ADOPT.

#### Utility Gate

Only after Safety Gate evaluation compare:

- tool calls;
- unique files opened;
- wall time;
- total tokens;
- retrieval footprint;
- setup/index cost;
- break-even estimate.

### Phase 11 — Produce artifacts and commit

Required output tree:

docs/experiments/codegraph-ab-2026-10/
- README.md
- manifest.json
- benchmark-prompts.json
- arm-map.json
- runs/
- answers/
- validation/
  - ground-truth.md
  - validation.json
  - CODEGRAPH_FAILURE_CASES.md
- metrics.csv
- FINAL-REPORT.md

The final commit MUST contain only permitted experiment artifacts and any necessary task-result metadata.

Do not commit .codegraph.

## SCOPE & FORBIDDEN ACTIONS

### In scope

- read-only repository exploration;
- isolated CodeGraph setup for the experiment;
- fresh child Codex session orchestration;
- blinded validation;
- metrics and evidence generation;
- final experiment artifact commit.

### Out of scope

- production implementation changes;
- bug fixes;
- refactors;
- schema changes;
- test rewrites;
- Phase-2 patch-generation benchmarking.

### Forbidden

Do NOT:

- modify this TaskContract;
- alter frozen benchmark prompts after measurement starts;
- reuse measured conversational contexts;
- leak one arm’s answer into another arm;
- globally rewrite Codex/MCP/AGENTS configuration for convenience;
- commit .codegraph;
- modify production source/tests;
- rerun an incorrect answer until it becomes correct;
- retry a genuine workload timeout merely to improve metrics;
- fabricate unavailable metrics;
- use CodeGraph as its own sole validator;
- hide setup/index cost;
- delete failure evidence;
- silently repair protocol violations.

## ACCEPTANCE CRITERIA

- AC-01: BENCHMARK_HEAD, repository state, environment, Codex version, model, reasoning, and CodeGraph version are recorded.
- AC-02: pre-measurement and post-measurement clean-state evidence exists.
- AC-03: exactly four valid prompts Q1–Q4 were frozen before measured execution and checksum recorded.
- AC-04: exactly 16 measured subject-session records exist, including timeout/error/protocol-violation records where applicable.
- AC-05: every measured run used a fresh non-resumed child Codex context/process.
- AC-06: corresponding A/B runs used the same BENCHMARK_HEAD, prompt, model, reasoning, and timeout.
- AC-07: Arm A had no CodeGraph access.
- AC-08: Arm B used isolated CodeGraph integration with no persistent/global instruction pollution.
- AC-09: CodeGraph setup/index time is reported separately from query time.
- AC-10: no measured child session silently modified repository content.
- AC-11: validation was independent and blinded, and did not use CodeGraph as sole ground truth.
- AC-12: correctness/dependency findings precede efficiency conclusions.
- AC-13: medians for tool calls, unique files opened, wall time, and tokens are reported where observable; unavailable fields are null/N/A.
- AC-14: retrieval footprint is reported where observable or explicitly marked unavailable.
- AC-15: CODEGRAPH_FAILURE_CASES.md exists.
- AC-16: FINAL-REPORT.md includes limitations and protocol deviations.
- AC-17: .codegraph is not committed.
- AC-18: production DevSopByAi source/runtime behavior was not changed.
- AC-19: final experiment artifacts are committed and FINAL_COMMIT is recorded.
- AC-20: ENGINEERING_DISPOSITION is evidence-based and uses one allowed value.

COMPLETE requires all applicable mandatory ACs to PASS.
If a structural precondition prevents a fair experiment, report BLOCKED rather than weakening an AC.

## EXECUTION EVIDENCE

The final artifact set MUST preserve enough evidence to audit and reproduce the experiment:

- Task ID and contract version;
- BENCHMARK_HEAD;
- initial/final repository status;
- CodeGraph setup/version/index evidence;
- frozen prompt checksum;
- actual run order;
- all 16 per-run JSON summaries;
- all subject answers;
- anonymous X/Y validation inputs or mappings sufficient to audit blinding;
- validator ground truth;
- validation metrics;
- metrics.csv;
- failure-case report;
- changed-files list;
- FINAL_COMMIT.

Evidence claims must be derived from observed output. Unknown values remain UNKNOWN/null/N/A.

## UNEXPECTED STATE POLICY

On unexpected state:

1. preserve evidence first;
2. do not modify the contract to make progress easier;
3. classify the issue as one of:
   - TRANSIENT_INFRASTRUCTURE
   - ENVIRONMENT_INCOMPATIBILITY
   - BENCHMARK_INVALIDITY
   - CODEGRAPH_LIMITATION
   - CODEX_LIMITATION
   - PROTOCOL_VIOLATION
4. continue only if experimental fairness remains intact;
5. otherwise stop as PARTIAL or BLOCKED.

If current CodeGraph/Codex CLI behavior differs from assumptions in this contract, adapt only the mechanics, not the invariants.

Non-negotiable invariants:

- same BENCHMARK_HEAD;
- same frozen prompt for corresponding A/B runs;
- same measured model/reasoning;
- fresh context;
- no unintended source mutation;
- independent blinded validation;
- unavailable metrics are not fabricated.

## TIMEOUT / RECOVERY POLICY

Measured child session:

- soft limit: 8 minutes
- hard limit: 12 minutes

At hard timeout:

- terminate the child;
- record TIMEOUT;
- preserve diagnostics;
- continue to the next scheduled run.

CodeGraph setup/index:

- hard limit: 20 minutes

If setup/index exceeds the hard limit:

- terminate it;
- preserve diagnostics;
- mark Arm B PARTIAL or BLOCKED as appropriate;
- continue only with evidence that remains meaningful.

Retry policy:

- maximum one retry;
- retry only for a clearly transient infrastructure/transport/process-start failure.

Do NOT retry because:

- an answer is wrong;
- CodeGraph gives a poor/empty result;
- logical analysis fails;
- a genuine workload hits timeout;
- a protocol violation occurs.

Every retry must be recorded with the reason.

## FINAL REPORT SCHEMA

FINAL-REPORT.md MUST contain:

- TASK_ID
- CONTRACT_VERSION
- STATUS: COMPLETE | PARTIAL | BLOCKED
- BENCHMARK_HEAD
- FINAL_COMMIT
- CHANGED_FILES
- CODEX_VERSION
- MODEL
- REASONING
- CODEGRAPH_VERSION
- CODEGRAPH_SETUP_SECONDS
- BENCHMARK_MATRIX
- COMPLETED_RUNS
- TIMEOUT_RUNS
- ERROR_RUNS
- PROTOCOL_VIOLATIONS
- CORRECTNESS_SUMMARY
- DEPENDENCY_RECALL
- CRITICAL_OMISSIONS
- UNSUPPORTED_EDGES
- MEDIAN_TOOL_CALLS
- MEDIAN_UNIQUE_FILES_OPENED
- MEDIAN_WALL_SECONDS
- MEDIAN_TOTAL_TOKENS
- RETRIEVAL_FOOTPRINT
- FIRST_USE_VIEW
- STEADY_STATE_VIEW
- BREAK_EVEN_TASKS
- CODEGRAPH_FAILURE_MODES
- LIMITATIONS
- PROTOCOL_DEVIATIONS
- AC-01 through AC-20 as PASS | FAIL | N/A
- ENGINEERING_DISPOSITION
- DISPOSITION_BASIS

ENGINEERING_DISPOSITION MUST be exactly one of:

- ADOPT
- ADOPT_WITH_GUARDRAILS
- DO_NOT_ADOPT
- INCONCLUSIVE

Disposition rules:

- ADOPT: Safety Gate passes and utility improvement is consistent enough to justify CodeGraph as the default discovery layer.
- ADOPT_WITH_GUARDRAILS: useful improvement exists, but critical paths require source/runtime revalidation or static-analysis gaps were observed.
- DO_NOT_ADOPT: material correctness regression, critical dependency loss, unacceptable operational cost, or no meaningful benefit.
- INCONCLUSIVE: evidence is insufficient or the protocol could not be completed fairly.

The final CodexC response to the user MUST be concise and include only:

- STATUS
- BENCHMARK_HEAD
- FINAL_COMMIT
- changed files
- AC summary
- ENGINEERING_DISPOSITION
- path to FINAL-REPORT.md
