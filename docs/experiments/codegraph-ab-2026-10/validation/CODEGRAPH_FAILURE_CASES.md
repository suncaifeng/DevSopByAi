# CodeGraph failure cases and observed limitations

This ledger includes setup-only and measured CodeGraph results. It does not claim that an unavailable or empty result is wrong unless the checked-in source independently establishes the contrary.

## Observed cases

1. **Wrong entry-point classification (setup preflight, outside the 16 measured sessions).** At `2026-10-02T03:03:11Z`–`03:04:23Z`, `codegraph_find_entry_points` classified `codex_run.py::_build_codex_command` at line 158 as `entry_type=cli_command`. The source shows this helper only builds a command; `main.py::__main__` deliberately exits and directs callers to `main(execution_input)`. The preflight answer repeated the wrong classification. Evidence: `setup/codegraph_mcp_preflight4_events.jsonl`, `setup/codegraph_mcp_preflight4_answer.txt`.

2. **Missing call-graph edges (measured Q1-R2-B).** Graph queries for `run_codex` (`codex_run.py:22`) and `route_decision` (`routing_system.py:19`) returned `callee_count=0` in summary mode, while source at those functions contains direct calls. The B answer used source reads to finish the path; the zero-callee result remained a CodeGraph miss. Evidence is summarized in `setup/failure-output-samples.json`; matching call IDs and arguments are in `runs/Q1-R2-B.json`.

3. **Workspace URI mismatch (measured Q4-R1-B).** A `codegraph_get_call_graph` call used a `file://` URI rooted at the per-run worktree, while the MCP index was rooted at the separate pinned index worktree. CodeGraph returned `Could not find symbol at location`. This is a path/configuration limitation in the isolated two-worktree setup; the model later used other graph queries and source reads. Evidence is in `setup/failure-output-samples.json` and `runs/Q4-R1-B.json`.

4. **MCP approval/configuration failure during setup only.** Initial setup preflights were denied while the CLI had `approval_policy=never`; the final isolated configuration enabled only 13 graph-navigation tools with per-server approval, after which the smoke query succeeded. No measured session failed for MCP startup. Evidence: `setup/codegraph_mcp_preflight.stderr`, `setup/codegraph_mcp_preflight3_terminal.log`, `setup/codegraph_mcp_preflight4_events.jsonl`.

5. **Higher retrieval and session cost in this matrix.** Across measured sessions, Arm B median tool output was 60,206 bytes versus Arm A's 48,609 bytes (+23.9%); median total token use was 273,669 versus 89,853 (+204.6%); and median wall time was 271.986s versus 187.748s. This is an observed arm-level difference; it does not isolate CodeGraph output from all other tool text.

## Not observed

- No stale-index result was observed; the indexed worktree and every measured worktree used `BENCHMARK_HEAD`.
- No installation or index failure remained after the setup-only approval/configuration issue was corrected.
- No related-test false positive was observed; CodeGraph returned empty related-test results and the checked-in repository has no tests.
- No macro or plugin-dispatch case exists in the selected Python behavior. Q4 exposed the workspace URI mismatch, but no additional runtime-only edge was attributed to CodeGraph.
- `unique_files_read` and `retrieval_tokens` were not observable in this environment and remain null/N/A.
