# TaskContract — MIG-0001 Runtime Truth Corrective Delta 01 — 2026-10-08

## METADATA
- TASK_ID: MIG-0001-RUNTIME-TRUTH-CORRECTIVE-DELTA-01-2026-10-08
- TASK_NAME: VM172 Local Control Plane and VM179 Live DevOps Read-Only Verification
- CONTRACT_VERSION: 1.0
- STATUS: READY
- REPOSITORY: suncaifeng/DevSopByAi
- AUTHORITATIVE_BRANCH: tasks/mig-0001-runtime-truth-corrective-delta-01
- TASK_PATH: docs/tasks/MIG-0001-RUNTIME-TRUTH-CORRECTIVE-DELTA-01-2026-10-08.md
- CREATED_FROM_REF: tasks/mig-0001-four-repo-legacy-evidence-audit
- CREATED_FROM_HEAD_VERIFICATION: BEFORE EXECUTION resolve the actual parent/fork commit SHA using git merge-base and git log; assert the fork is a descendant of MIG-0001 audit evidence commit and record exact SHA in evidence. No guessed SHA is permitted.
- PARENT_TASK: docs/tasks/MIG-0001-FOUR-REPO-LEGACY-EVIDENCE-AUDIT-2026-10-08.md
- PARENT_TASK_BLOB: 337d963d62988c084809c082bca48a47c4faa66a
- PARENT_REPORT: migration/MIG-0001/final-report.md
- PARENT_RESULT: PARTIAL
- ASSIGNEE: CodexC
- RECOMMENDED_MODEL: GPT-5.6 Terra
- REASONING: medium
- ESTIMATED_EXECUTION_TIME: 45-90 minutes
- NORMAL_LIMIT: 120 minutes
- MODE: READ_ONLY_RUNTIME_AUDIT
- CONTRACT_IMMUTABLE: true
- GPU_REQUIRED: false
- VM_POWER_MUTATION: forbidden
- MAIN_MERGE: forbidden

## 1. SCOPE AND FACT CORRECTIONS
MIG-0001 completed Git inventory but left VM172 and VM179 unverified. User confirms:
- VM172 (.72) is the current Codex host and AI Control plane. Prefer LOCAL inspection; do not route through VM176 to SSH back into VM172.
- VM179 (.79) was powered off during MIG-0001 but user HAS NOW POWERED IT ON. Its former 'No route to host' was not proof of network misconfiguration; verify its present live state now.
- VM176 (.76) is the V100 runtime, currently subject to an independent bounded thermal test task owned by CodexB. This Delta must not interfere with the GPU, power limit, ComfyUI, CodexB, or watchdog.
User confirmations are contextual declarations; capture new live evidence rather than asserting a current VM state without checking.

Goal: close the narrow control-plane / DevOps runtime evidence gaps and confirm authoritative Supervisor/GPU lease ownership before advancing to MIG-0002 design. No repo migrations or production changes.

## 2. START GATE
- Validate repository origin, exact branch, this immutable TaskContract Git blob, parent TaskContract blob and parent report Git identities, authorized isolated clean worktree, and real initial HEAD with full SHA; if fork SHA cannot be verified stop BLOCKED_IDENTITY.
- Log actual Codex execution hostname and IP(s), user, process executable and version, current worktree/SSH context. If running on VM172, inspect VM172 locally. If not, do not assume it is VM172; mark discrepancy and use only existing approved trust path, not insecure SSH flags.
- Confirm VM179 now responds at the intended address and verify hostname / guest identity; 'powered on' does not automatically mean SSH credentials or services available.
- Acquire NO GPU lease and request NO GPU work; use read-only checks only. Do not alter CodexB thermal experiment in progress.
- No interactive credentials; no edits to known_hosts, authorized_keys, network policies, PVE power state or system services.

## 3. EXACT EXECUTION PLAN
A. VM172 local evidence:
1. Run safe, bounded local commands to verify host, OS/kernel, interfaces/IP, local Codex CLI installation/availability, invoking user, active Codex sessions, repository worktrees and Git origins.
2. Enumerate only relevant task supervisor/relay systemd units/timers/processes (enabled/active state), associated task identities, running/durable launch markers, ownership locks, source/target Git branch references, queue/launcher capability and last-known terminal state.
3. Collect redacted configuration metadata and immutable hashes; NEVER print environment secrets, SSH keys, auth JSON, tokens, sudoers contents or credential values.
4. Check whether VM172 is in fact exercising task dispatch authority and whether VM176 old holiday relay has any overlapping current ownership; do not start/stop either.
B. VM179 newly-online verification:
5. From VM172/current Codex host use existing trusted noninteractive SSH method; verify target VM179 at .79 by host key + hostname before collecting details; fail closed if trust mismatch.
6. Inspect VM179 OS, Codex/version presence (do not install), Git workspace paths/origins/worktrees, services related to DevOps jobs, disk/memory capacity, route/reachability, developer tool availability, task dispatcher/service overlap, and active workloads, all read only.
7. If SSH fails, distinguish routing, network reachability, known_hosts trust and authentication; no repair, installation, or privilege escalation.
C. Cross-VM controller truth:
8. Read-only verify VM176 relay status and durable exactly-once markers via existing trusted access IF available without colliding with CodexB; read-only GPU service/lease process ownership snapshot only when noninterfering. If CodexB is running, do not inspect private mutable test state or acquire locks. Prefer rely on MIG-0001 preserved VM176 snapshot and label present runtime changes as not independently verified rather than interfere.
9. Build explicit controller authority matrix: VM172 Control Plane; VM179 Development Execution Plane; VM176 GPU Runtime Plane. Identify double Supervisor/fencing, concurrent launcher, power manager and GPU lease hazards. Resolve only with evidence; do not claim 'no duplicate' from a missing VM172/VM179 observation.
D. Evidence and gating:
10. Reconcile parent findings without modifying existing reports. Treat 'VM179 previously offline' as a historical observation, replace with timestamped current result only in a new Delta report.
11. Record remaining UNKNOWN/BLOCKED items, evidence hashes, owner/host identity and time. Recommend MIG-0002 DESIGN_ONLY gate if key authority risk is adequately documented; no authorization for repository creation, code migration or cutover.
12. Validate JSON/CSV/Markdown and file allowlist, commit and guarded non-force fast-forward push on exact branch, then STOP for independent GPT Review.

## 4. SCOPE & FORBIDDEN ACTIONS
Only authorized new files under migration/MIG-0001/delta-01/** and this TaskContract; do not edit original MIG-0001 outputs, old contracts, source repository, MIG-0002, production configs, GPU power/thermal settings, running Codex sessions, active GPU workloads, systemd states, process state, VM power state, SSH trust settings, firewall or storage. No deletion, branch rewrite, merges, force push, model downloads or long scans. Host commands must be short, read-only and time-bounded. If host unavailable, record UNKNOWN and continue other independent tasks.

## 5. ACCEPTANCE CRITERIA
AC01 Repo, branch, immutable Task blob, parent blob and fork commit verified from Git; no ambiguous lineage.
AC02 Real Codex host identity checked; VM172 local Control Plane evidence collected if actually local.
AC03 VM172 active/inactive supervisor processes, launcher, Git worktrees, ownership and durable markers characterized without modifying them.
AC04 VM179 now-on state LIVE VERIFIED with host identity, SSH trust, tool/worktree/service inventory, or precise blocked reason.
AC05 VM176 relay/GPU ownership conflict reviewed without interfering with concurrent CodexB work.
AC06 No dual-authority conclusion asserted without actual evidence; controller/fencing recommendation explicit.
AC07 Runtime Truth report explicitly separates USER_REPORTED, LIVE_VERIFIED, GIT_REPORTED and UNVERIFIED with UTC timestamps and evidence source.
AC08 All files confined to allowlist; original MIG-0001 output hashes unchanged; no production/VM/Git-side effects except new Delta evidence branch.
AC09 Machine-readable evidence, syntax/cross-reference checks and a truthful COMPLETE/PARTIAL/BLOCKED report with exact HEAD/commit.
AC10 MIG-0002 recommendation confined to design-only, subject to independent review; no automatic next task execution.

COMPLETE requires all mandatory ACs PASS and sufficient safe runtime evidence; otherwise PARTIAL/BLOCKED. A powered-on VM179 alone does not satisfy AC04.

## 6. OUTPUTS / EXECUTION EVIDENCE
- migration/MIG-0001/delta-01/vm172-local-truth.md
- migration/MIG-0001/delta-01/vm179-live-truth.md
- migration/MIG-0001/delta-01/controller-authority-matrix.md
- migration/MIG-0001/delta-01/runtime-reconciliation.json
- migration/MIG-0001/delta-01/evidence-manifest.json
- migration/MIG-0001/delta-01/final-report.md

Capture actual input ref SHA, original evidence immutable Blob SHA, UTC host observation timestamps, redacted command evidence and output SHA256. Final report: RESULT, TASK_ID, START_HEAD, END_HEAD, COMMIT, CHANGED_FILES, AC01–AC10, VM172_RESULT, VM179_RESULT, VM176_CROSSCHECK, CONTROLLER_AUTHORITY, KNOWN_GAPS, NEXT_GATE.
Max 120 minutes; if blocked on connectivity/identity, record evidence and close rather than waiting without bound.

## 7. UNEXPECTED STATE POLICY
Hard STOP on wrong host identity, Task blob alteration, unexpected worktree conflict, suspected credential exposure or production-process/GPU intervention. Soft failure for unavailable VM179 SSH, partial read permissions, VM176 busy with thermal test; do not ask user interactively or remediate. Fail closed on duplicate supervisor authority and mark unresolved risk. Stop after independent-review handoff.

## 8. LAUNCH_PROMPT
You are CodexC. Work in suncaifeng/DevSopByAi on dedicated branch tasks/mig-0001-runtime-truth-corrective-delta-01. Execute ONLY immutable TaskContract docs/tasks/MIG-0001-RUNTIME-TRUTH-CORRECTIVE-DELTA-01-2026-10-08.md. Verify exact current fork/head and immutable parent contract. VM172 (.72) is the Codex host per user: inspect the actual local host first; VM179 (.79) has now been powered on and requires trusted SSH live verification. Read-only audit of Supervisor/launcher/DevOps/control ownership, avoid all interference with CodexB V100 thermal test on VM176. No restarts, VM power changes, auth/network changes, GPU workloads or migrations. Write only migration/MIG-0001/delta-01/** evidence; guarded commit/push; STOP for independent GPT Review.
