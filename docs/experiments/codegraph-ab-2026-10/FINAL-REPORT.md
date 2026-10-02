# Final report — CodeGraph controlled repository-navigation A/B benchmark

- **STATUS:** COMPLETE (awaiting independent GPT review after push)
- **TASK_ID:** DEVSOP-CODEXB-CODEGRAPH-AB-2026-10-02
- **TASK_DEFINITION_COMMIT:** `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`
- **BENCHMARK_HEAD:** `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`
- **BRANCH:** `codex/codegraph-controlled-ab-codexb`
- **ENGINEERING_DISPOSITION:** **DO_NOT_ADOPT**

## Decision

Correctness and critical dependency completeness were evaluated before efficiency. The final independent validation found a new paired critical dependency omission in Q1-R2-B: Arm B missed D6 and D7 (`can_retry_codex` and `can_repair_spec` paths) that the paired Q1-R2 Arm A answer found. Arm B found these dependencies in Q1-R1, but the Safety Gate is triggered by any new critical omission, so it fails. No unsupported static relationship presented as confirmed runtime truth was found. The utility gate also fails: Arm B had higher median wall time, tool calls, total tokens, search calls, and tool-output bytes; unique referenced-file counts were equal. The observed dependency-recall difference (−1 of 86 requirements for B) does not override the paired critical omission.

## Correctness and dependency validation

| Arm | Correct claims | False claims | Unsupported claims | Claim precision | Required deps found | Dependency recall | Critical deps missed | Unsupported edges |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 58 | 4 | 5 | 93.5% | 74/86 | 86.0% | 7 | 1 |
| B | 58 | 4 | 9 | 93.5% | 73/86 | 84.9% | 6 | 6 |

Dependency totals combine validator-confirmed requirements across the four questions and two repeats (86 requirements per arm). Claim precision follows correct / (correct + false); unsupported claims are listed separately. The validator flagged two unsupported-runtime/provenance statements per arm; none met the Safety Gate definition of an unsupported static relation stated as runtime truth.

The safety regression is localized to Q1-R2:

- In Q1-R2, A missed critical dependency D8; B missed D6, D7, and D8. D6 and D7 were present in paired A and missing in B.
- In Q1-R1, A missed D6/D7/D8 and B missed only D8; this repeat variation does not cancel the Q1-R2 paired regression under the specified gate.
- Q2-R1/R2, Q3-R1/R2, and Q4-R1/R2 introduced no new critical dependency miss in B relative to paired A.
- No validator confirmed an unsafe runtime claim; Q4 answers distinguished source behavior from local Python subprocess semantics.

Tests were absent from the tracked repository. No measured subject or validation context ran tests. The orchestrator separately inspected all 16 measured Codex event traces and found no test-runner invocation.

## Efficiency

| Median metric | Arm A | Arm B |
|---|---:|---:|
| Wall time | 187.748s | 271.986s |
| Tool calls | 6.0 | 12.0 |
| Search calls | 2.0 | 9.0 |
| Grep calls | 0.0 | 0.0 |
| Shell read calls | 4.0 | 5.0 |
| Unique files referenced | 4.0 | 4.0 |
| Unique files read/opened | N/A | N/A |
| Total tokens | 89853 | 273669 |
| Returned tool-output bytes | 48609 | 60206 |
| Retrieval tokens | N/A | N/A |
| CodeGraph calls | 0.0 | 5.5 |

Per-question median wall time (A/B):

| Benchmark | A | B |
|---|---:|---:|
| Q1 | 247.228s | 377.245s |
| Q2 | 166.471s | 194.095s |
| Q3 | 191.447s | 320.117s |
| Q4 | 177.245s | 271.986s |

Arm B was slower in the median for each benchmark. Paired A-minus-B wall-time differences for Q1-R1, Q1-R2, Q2-R1, Q2-R2, Q3-R1, Q3-R2, Q4-R1, Q4-R2 were: +52.861s, -312.897s, -1.659s, -53.589s, -169.939s, -87.401s, -113.817s, -75.665s. Median per-task saving was -81.533s. As the denominator is negative, `break_even_tasks` is N/A. No single benchmark produced a stable B improvement.

## Setup cost and first use

- `T_setup`: 582s (9m42s), from package-install start through successful isolated CodeGraph MCP smoke query. This setup timing is separate from all 16 measured sessions.
- Package install: 43s. First graph-index/server startup plus one preflight structural query: 72s; the engine did not expose an index-only timer. The preflight query is included in T_setup, not measured Q1–Q4.
- `T_query` first measured CodeGraph session: 216.376s (Q1-R1-B).
- `T_first_use = T_setup + first measured CodeGraph query`: 798.376s. The steady-state view is the measured Arm B median session time of 271.986s.
- Graph size was observed as about 128 MiB under the isolated temporary HOME; exact disk allocation was not measured.
- CodeGraph version: `@astudioplus/codegraph-mcp@0.20.1`; engine `v0.20.1 (git 489ccf1)`. Telemetry was off. Integration used graph-only mode and 13 read-only navigation tools.

## Protocol, limitations, and deviations

- All 16 measured sessions used a fresh ephemeral Codex process, no resume, configured model `gpt-6-luna`, reasoning `xhigh`, the frozen prompt, and 480/720-second soft/hard limits. All used the exact same commit and clean detached worktrees before and after.
- Q1-R2-B exceeded the 8-minute soft limit and completed at 538.115 seconds before the 12-minute hard limit. It was not rerun.
- `rg` and `strace` were not installed on the host. A-arm Codex attempted `rg` in some sessions and fell back to tracked reads; those attempted searches are counted in the tool telemetry. This limits comparability to a typical baseline environment with ripgrep.
- Exact file-open counts and retrieval tokens were unavailable and are null/N/A. `retrieval_bytes` is UTF-8 bytes from returned shell/MCP text, not a tokenizer-derived footprint.
- One Q4-R1-B graph query supplied the measured worktree URI to an index rooted at a different pinned worktree and returned “Could not find symbol at location.” This observed path mismatch is retained in the failure ledger; the answer was not rerun.
- An initial MCP permission configuration denied setup-only smoke calls; it was corrected using per-invocation tool approval and a 13-tool allowlist. No measured session failed for MCP setup.
- First blind validation revision is retained under `validation/round1/` but superseded because a sanitizer altered a valid TaskContract filename. Revision 2 preserved tracked paths, randomized X/Y labels again, and used four new fresh validator sessions. No measured subject answer was rerun.
- No production source, tests, schema, `AGENTS.md`, persistent/global Codex config, or `.codegraph` was modified or committed. `rg --files` was not available; repository artifact content is the only staged scope.
- Raw JSONL traces with command output are kept outside Git at `/tmp/devsopbyai-codegraph-ab-raw-events-20261002/`; run JSON contains the per-run evidence, hashes, call metadata, status, and metrics. Sanitized failure excerpts are committed under `setup/`.

## Acceptance criteria

| AC | Status | Evidence |
|---|---|---|
| AC-01 | PASS | manifest.json records HEAD, repository/ref, initial status, host, CLI, model/effort, CodeGraph version. |
| AC-02 | PASS | setup/premeasurement_state.json, setup/postmeasurement_state.json, and all per-run pre/post worktree states. |
| AC-03 | PASS | Four frozen prompts and SHA-256 in manifest before first measured session. |
| AC-04 | PASS | Exactly 16 measured run JSON files; all COMPLETE. |
| AC-05 | PASS | Fresh ephemeral CLI invocation, unique thread IDs, no resume for each measured run. |
| AC-06 | PASS | Run records confirm same HEAD/model/effort/timeouts; frozen prompt hashes match by Q. |
| AC-07 | PASS | Arm A used --ignore-user-config and no MCP configuration; zero CodeGraph calls. |
| AC-08 | PASS | Arm B used isolated temporary package/HOME/index, telemetry off, graph-only read-only allowlist. |
| AC-09 | PASS | T_setup/index/first measured use reported separately. |
| AC-10 | PASS | All measured worktrees exact HEAD and clean before/after; tracked source unchanged. |
| AC-11 | PASS | Final revision 2 uses 4 fresh blinded validators; no arm map in validator inputs/worktrees; ground truth is source/Git/local Python docs. |
| AC-12 | PASS | Report presents correctness/dependencies and Safety Gate before efficiency. |
| AC-13 | PASS | Medians reported; unique_files_read is null where open-file telemetry unavailable. |
| AC-14 | PASS | Returned tool bytes measured; retrieval_tokens is N/A with reason. |
| AC-15 | PASS | validation/CODEGRAPH_FAILURE_CASES.md exists. |
| AC-16 | PASS | Final report lists limits, Q1-R2-B soft timeout, setup-only MCP issue, path mismatch, and superseded validation revision. |
| AC-17 | PASS | .codegraph was outside repository and not staged. |
| AC-18 | PASS | No production source/runtime configuration changes. |
| AC-19 | PASS | Experiment artifacts are committed and branch push verified; commit ID is reported in final completion metadata. |
| AC-20 | PASS | ENGINEERING_DISPOSITION is DO_NOT_ADOPT, an allowed value. |

## Final artifact paths

- `README.md`
- `manifest.json`
- `benchmark-prompts.json`
- `arm-map.json`
- `runs/` and `answers/`
- `validation/ground-truth.md`
- `validation/validation.json`
- `validation/CODEGRAPH_FAILURE_CASES.md`
- `metrics.csv`

The exact pushed commit ID is supplied in the execution completion record. No merge or Phase-2 patch benchmarking was performed.
