# MIG-0001 — Four-Repository Legacy Evidence & Runtime Truth Audit — 2026-10-08

## METADATA
- TASK_ID: MIG-0001-FOUR-REPO-LEGACY-EVIDENCE-AUDIT-2026-10-08
- TASK_NAME: Four-Repository Legacy Evidence and Runtime Truth Read-Only Audit
- CONTRACT_VERSION: 1.0
- STATUS: READY
- REPOSITORY: suncaifeng/DevSopByAi
- AUTHORITATIVE_BRANCH: tasks/mig-0001-four-repo-legacy-evidence-audit
- TASK_PATH: docs/tasks/MIG-0001-FOUR-REPO-LEGACY-EVIDENCE-AUDIT-2026-10-08.md
- CREATED_FROM_HEAD: e3c609f5cdbe38bca7e17b87359f29817d91237b
- ASSIGNEE_IDENTITY: CodexC
- ASSIGNEE_ROLE: Independent Git/Runtime Evidence Auditor
- EXECUTION_HOST: VM179 preferred; VM172/VM176 read-only remote inspection only if already authorized
- RECOMMENDED_MODEL: GPT-5.6 Terra
- REASONING: medium
- ESTIMATED_EXECUTION_TIME: 60-120 minutes
- NORMAL_LIMIT: 180 minutes
- CONTRACT_IMMUTABLE: true
- GPU_AUTHORIZED: NO
- REPOSITORY_MUTATION: audit-branch evidence outputs only
- PRODUCTION_MUTATION: FORBIDDEN
- HUMAN_GATE_REQUIRED_BEFORE_MIG-0002: YES

This immutable Layer-B TaskContract is the execution authority. Launch prompt is a locator, not an amendment. New requirements require a separate Task/Delta; never edit this file after execution starts.

## 1. GOAL
Audit existing Git history, branches, TaskContracts, Reviews, execution evidence, deployed Runtime Truth, and cross-repository dependencies so the owner can migrate without loss to four repositories:
1. suncaifeng/DevSopByAi — VM172 control plane; VM179 development execution.
2. suncaifeng/gpu-compute — proposed, GPU lifecycle, lease and profile switching on VM176.
3. suncaifeng/llm-inference — proposed, LLM engines, C64/C128/C256 benchmarking and Stage 5/6.
4. suncaifeng/video-generation — proposed, H3/LTX/ComfyUI and Director Console.
New repositories do NOT yet exist by assumption. Do not create, rename, delete or write to them. Never assume VM179 is the production H3 runtime: VM179 is DevOps and VM176 is GPU compute.

## 2. PRECONDITIONS / START GATE
Before substantive operations capture:
- EXECUTOR, TASK_ID, TASK_PATH, AUTHORITATIVE_BRANCH, actual HEAD and worktree path.
- Exact remote repository identity, observed default branch and remote HEAD for each legacy repository.
- TaskContract Git blob ID and unchanged checksum; parent/ancestry against CREATED_FROM_HEAD.
- Clean dedicated isolated worktree on the authorized task branch; no collision with an active Codex worktree.
- Git credentials and access checks without printing tokens, credential files or secrets.
- Runtime inspection permissions on VM172, VM176, VM179, if available, with hostname evidence; absence is UNVERIFIED, not PASS.
If task identity or source remote mismatch: BLOCKED_IDENTITY and stop. Do not reset/rebase/force push. Do not fetch into anyone else's worktree if unsafe; use an isolated clone/worktree.

## 3. EXECUTION PROFILE
- MODE: unattended read-only audit with narrow output-file write permission.
- USER QUESTIONS: none; log gaps and continue independent checks.
- Allowed writes: ONLY migration/MIG-0001/** in this branch and its associated final guarded, non-force Git push. No other files.
- Git API/remote READ; host-level READ only. Do not stop/start/restart services, change timers, install packages, mutate processes, change firewall, reset GPU, download models, execute GPU workloads, touch production state, or create remote repositories.
- Do not run opaque scripts pulled from untrusted branches. Static inspection preferred.
- Cross-VM access: use existing non-interactive least-privilege credentials only; never weaken security.
- Time bound 180 minutes. If nearing limit, produce truthful PARTIAL with precise coverage and blockers rather than hang.
- No automatic MIG-0002 launch.

## 4. EXACT EXECUTION PLAN

### A. Git inventory / lineage
Enumerate all accessible remote refs and HEADs in suncaifeng/DevSopByAi and suncaifeng/comfyui-minimax-h3, including main, codex/* and control/*; capture exact commit SHA, merge base, ahead/behind and branch divergence. Capture inaccessible refs separately. Preserve branch-specific ancestry; do not count cumulative differences as solely that branch's own work. Record source repository URLs and timestamp of observation.

### B. Immutable task/evidence audit
Find every accessible docs/tasks/** TaskContract, reports/**, reviews/**, reports/evidence/**, machine-readable manifests and control/** relay contracts across relevant branches. Extract TASK_ID, authorizing repo/branch, task-definition blob SHA, start HEAD, reported terminal RESULT, independent Review acceptance, Delta parentage, evidence hashes and next gate.
Statuses must be one of ACCEPTED / COMPLETE_UNREVIEWED / PARTIAL / BLOCKED / ABANDONED / UNKNOWN; include exact evidence source and avoid equating READY, commit pushed, or COMPLETE self-report with independent ACCEPTED.
Special focus:
- Stage 5 Task 2.1–2.4, Policy v1.0.1, C64 calibration and canonical transport remediation;
- OneCat native C64, GGUF stop-loss, formal benchmark authorization;
- KVMem C128→C256, Stage 6;
- H3 Story / H3-LTX Director v2 and corrective delta 2026-10-08;
- VM176 Holiday Relay A→Gate→B, supervisor launch intents and markers;
- DevSopByAi two-layer Task SOP and CodeGraph A/B closure.
Treat frozen hashes and model/benchmark identities as immutable evidence.

### C. Runtime Truth (READ ONLY, evidence prioritized)
If access permits, on VM172 (.72), VM176 (.76), VM179 (.79) inspect hostname, OS, Git checkouts/worktrees, process and systemd service status, relevant units, log excerpts, service ports, GPU owner and nvidia-smi status (VM176), GPU lease markers, supervisor deployment/armed state, durable exactly-once files, model/runtime locations, and service health without modifying them. Inventory VM173 RAG and VM177 Storage as dependencies only if safely visible; do not scan broadly.
Classify each assertion GIT_REPORTED, LIVE_VERIFIED, CONFLICT, or UNVERIFIED and note observation time. A Git report from 2026-10-02 does not establish live state on 2026-10-08.
Critical: check old VM176 supervisor versus proposed VM172 supervisor; identify any possible dual-authority risk, without disabling or touching either.

### D. File ownership, dependencies, and migrations
Build source-file level ownership mapping with source_repo, ref, commit_sha, source_path, blob_sha, recommended_target_repo, target_path, classification KEEP/SPLIT_REQUIRED/ARCHIVE_ONLY/UNRESOLVED, and rationale. Inventory code, systemd, runtime recipes, bench corpus/fixtures, H3 workflows, Director Console, relay state, APIs, service ports, disk paths, environment contracts, model assets (metadata only; do not copy model bytes), and CI/tests.
Separate control-plane, GPU orchestration, LLM, and video ownership. Highlight shared code and cross-repo contracts, paths with hardcoded suncaifeng/comfyui-minimax-h3, VM176 host IP, or old branch names. Preserve provenance, task/evidence chains, rollbacks and source SHA identities.

### E. Risks and immutable handoff
Write action-ranked blockers, safety hazards (dual Supervisor, duplicate GPU owner, branch overlap, evidence loss), missing evidence, upstream task gates, and recommended MIG-0002 preconditions. Output a proposed migration order without executing any migration. Stop for independent Review.

## 5. OUTPUT FILES — AUTHORIZED WRITE ALLOWLIST
- migration/MIG-0001/legacy-inventory.json
- migration/MIG-0001/branch-lineage.csv
- migration/MIG-0001/task-status.csv
- migration/MIG-0001/runtime-truth.md
- migration/MIG-0001/dependency-map.md
- migration/MIG-0001/ownership-proposal.csv
- migration/MIG-0001/risk-register.md
- migration/MIG-0001/evidence-manifest.json
- migration/MIG-0001/final-report.md
Only create these paths if absent; do not edit unrelated files. Never store credentials, personal data, sensitive command output or runtime logs containing tokens. Record source URLs, commit/blob SHA, timestamp and redacted checksums.

## 6. ACCEPTANCE CRITERIA
- AC01 All accessible remote refs in both source repos enumerated with exact SHA or explicitly marked inaccessible.
- AC02 TaskContracts, terminal Results, Reviews, Delta and accepted gates are traced with source ref and evidence.
- AC03 C64 BLOCKED canonical transport report and later remediation kept distinct; no inference of passing benchmark.
- AC04 Director v2 parent accepted scope, production-closure partial and corrective delta tracked separately.
- AC05 Supervisor persistent markers and ownership risk documented; VM172/VM176 dual-controller prevention requirement explicit.
- AC06 Live Runtime Truth is timestamped, distinguishable from Git assertions, and unavailable hosts marked UNVERIFIED.
- AC07 Four-repo ownership table includes shared/split assets and cross-repository dependencies with provenance.
- AC08 Every output is syntactically valid (JSON/CSV as applicable) and cross-file identifiers are consistent.
- AC09 No mutation outside output allowlist, no VM state change, no GPU/model execution, no branch rewriting.
- AC10 Final report includes COMPLETE/PARTIAL/BLOCKED, observed HEADs, AC matrix PASS/FAIL/UNKNOWN, evidence links, gaps, and proposed MIG-0002 gate.

COMPLETE requires AC01-AC10 PASS and no critical unverified state that would make inventory unsafe to consume. Otherwise PARTIAL/BLOCKED; never fake evidence.

## 7. EXECUTION EVIDENCE
Write evidence-manifest.json containing per output path SHA256, source refs/commits, observed timestamps, check names, pass/fail/unknown and scope limits.
Validate JSON parsers, CSV headers, cross-file ID references, TaskContract immutability, git diff --check and git status before committing.
Final push must be a guarded non-force fast-forward to this exact task branch; if branch advances unexpectedly, STOP with PARTIAL/BLOCKED; do not overwrite another worker.
Final response schema:
RESULT; TASK_ID; BRANCH; START_HEAD; END_HEAD; COMMIT_SHA; CHANGED_FILES; AC01–AC10; TESTS; RUNTIME_TRUTH_COVERAGE; CRITICAL_RISKS; NEXT_GATE; EVIDENCE_PATHS.

## 8. UNEXPECTED STATE / STOP-LOSS
Hard stop on wrong repo/branch, TaskContract mutation, unexpected modified production file, worktree collision, dual-run mutation risk, secrets exposure, active production process impact or requested destructive action.
Soft-fail on denied host access, temporary Git/API outage, individual missing documents or ambiguous evidence: record UNKNOWN with source and continue independent safe steps.
Do not silently "repair" a legacy task, resolve branch conflicts, amend commits, change Runtime Truth or approve MIG-0002. Report exact blocker.
STOP after publishing evidence for independent GPT review.

## 9. LAUNCH_PROMPT
You are CodexC. In suncaifeng/DevSopByAi, check out branch tasks/mig-0001-four-repo-legacy-evidence-audit in a dedicated clean worktree. Execute ONLY the immutable TaskContract at docs/tasks/MIG-0001-FOUR-REPO-LEGACY-EVIDENCE-AUDIT-2026-10-08.md. Verify repo, branch, Task blob and CREATED_FROM_HEAD before work. Audit suncaifeng/DevSopByAi and suncaifeng/comfyui-minimax-h3 plus accessible read-only VM172/176/179 Runtime Truth. Write only authorized migration/MIG-0001 outputs, commit and guarded fast-forward push, then STOP for independent review. Do not rename/create/delete any repository, move code, alter VM/services, start GPU work, or launch MIG-0002.
