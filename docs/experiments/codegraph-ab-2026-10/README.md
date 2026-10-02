# Controlled CodeGraph repository-navigation A/B benchmark

- Task: `DEVSOP-CODEXB-CODEGRAPH-AB-2026-10-02`; TaskContract `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`.
- Branch: `codex/codegraph-controlled-ab-codexb`; frozen `BENCHMARK_HEAD`: `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`.
- Matrix: 4 benchmarks × 2 repeats × 2 arms = 16 fresh, ephemeral subject sessions. All 16 completed; no measured retry, hard timeout, or dirty worktree.
- Subject model/effort: `gpt-6-luna` / `xhigh`; soft/hard timeout: 480/720 seconds.
- CodeGraph: `@astudioplus/codegraph-mcp@0.20.1`, engine `v0.20.1 (git 489ccf1)`, telemetry off, graph-only and 13 read-only navigation tools, per-invocation MCP configuration. Arm A had no MCP configuration or CodeGraph access.
- Prompts: `benchmark-prompts.json`, SHA-256 `04db480fd7e7638e15b6b70a5d48e54d71fb1780d69c20d99e7916a9c5d6c62a`; frozen before measurement.
- Validation: four fresh independent, blinded validator sessions, one per question, with no CodeGraph MCP. Final validation revision 2 is in `validation/`; the first validator output is retained under `validation/round1/` and marked superseded because an anonymizer changed a valid TaskContract filename. No measured answer was rerun.
- Engineering disposition: **DO_NOT_ADOPT**. Q1-R2-B introduced two paired critical dependency omissions, and Arm B had higher median latency, tool calls, tokens, and returned tool-output bytes. See `FINAL-REPORT.md`.

## Artifact map

- `manifest.json`: task identity, frozen state, setup, run matrix, environment, hashes, and final status.
- `benchmark-prompts.json`: the four frozen prompts.
- `arm-map.json`: X/Y to A/B mapping, kept out of validator worktrees and prompts.
- `runs/`: one JSON record per measured session.
- `answers/`: unmodified final answer text from measured sessions.
- `validation/ground-truth.md`: source-grounded dependency sets and answer review.
- `validation/validation.json`: all dependency/claim results, paired gate, and aggregates.
- `validation/CODEGRAPH_FAILURE_CASES.md`: observed CodeGraph output, workspace path, setup, and retrieval-cost issues.
- `metrics.csv`: per-run scores and per-arm/per-question medians.
- `setup/`: preflight, version, package install, index, and state evidence.

## Metric definitions and capture limits

Tool calls, search calls, grep calls, shell read calls, CodeGraph calls, token usage, and returned tool-output bytes were computed from Codex JSONL events. `unique_files_referenced` counts tracked paths present in the final answer. Exact file-open events were unavailable because `strace` is not installed, so `unique_files_read` is null. `retrieval_tokens` is null because no retrieval tokenizer was available. Empty CSV fields represent null/N/A.

`T_setup` is reported separately from measured `T_query`. It includes package installation, isolated MCP configuration/troubleshooting, graph indexing, and the first smoke query; the server did not expose a separate index-only timer.
