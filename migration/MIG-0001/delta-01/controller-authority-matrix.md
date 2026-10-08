# Controller / Launcher / Runtime Authority Matrix

Observation window: `2026-10-08T08:05:17Z`–`08:09:55Z` UTC for VM172 and VM179. VM176 current runtime was intentionally not queried to avoid interfering with CodexB or GPU work.

| Plane / host | Declared role | Fresh evidence | Supervisor / launcher authority | GPU lease / workload authority | Status |
|---|---|---|---|---|---|
| VM172 `.72` / `ai-control` | **USER_REPORTED:** Control Plane; current Codex host | **LIVE_VERIFIED:** local Debian 13 host; Codex CLI 0.155.1; three active Codex process pairs. No matching system/user systemd services or timers, no task IDs in filtered process argv, and no matching marker directories in bounded paths. | Codex CLI and interactive sessions exist. No durable Supervisor, dispatcher, queue, launch intent, or ownership marker was identified. Actual task-dispatch authority and the task identity of the active sessions remain **UNVERIFIED**. | No GPU workload or GPU lease was inspected or claimed on VM172. | Live host verified; durable controller authority unresolved. |
| VM179 `.79` / `devops` | **USER_REPORTED:** Development Execution Plane | **LIVE_VERIFIED:** fresh trusted SSH; host online and identified; Git/Python available; Codex absent; no matching DevOps units, worker processes, dispatcher, listener, marker directory, or DevSop workspace in bounded roots. | No current DevOps launcher or task-dispatch service was observed. VM179 currently cannot be treated as a verified Codex launcher host. | No GPU role or GPU lease observed. | Live host verified; no active task executor found. |
| VM176 `.76` / `compute` | **USER_REPORTED:** GPU Runtime Plane; may be used by CodexB for an independent V100 thermal test | **GIT_REPORTED** from immutable MIG-0001 `runtime-truth.md` (blob `edebc6133e5c3b9586deeaf9bc6c7257a1d039eb`), observations at `2026-10-08T07:21:19Z` and `07:34:02Z`: `vm176-holiday-relay.service` disabled/inactive; dry-run state suppressed launch; `codexb.launch.intent` and `codexb.launched` absent at that time; `ai-comfyui` owned the GPU. H3 thermal preflight report later self-reported BLOCKED before workload/power changes. | Historical relay state does not establish present state. No current VM176 service, marker, CodexB, or process state was inspected in this Delta. Current ownership is **UNVERIFIED**. | Prior snapshot reported ComfyUI as GPU owner and no approved exclusive lease. Current CodexB/thermal/GPU lease state is **UNVERIFIED**; do not acquire a lease or inspect private mutable test state. | Historical snapshot reviewed; current state intentionally not verified. |

## Authority conclusion

No evidence establishes an active duplicate Supervisor, but the available observations also do **not** prove single-controller fencing. VM172 is confirmed as the Codex host but its active Codex sessions have no discoverable task IDs or durable dispatch markers. VM179 is online but has no Codex CLI or DevOps task service. The VM176 snapshot is historical and may no longer describe the thermal-test window.

Treat actual controller ownership as **UNRESOLVED / OPEN BLOCKER**. Do not launch a task or GPU workload based on this matrix.

## Required design gate before MIG-0002

1. Designate one durable task Supervisor and define its exact host, unit, source commit, queue, and marker paths.
2. Design fencing so the VM172 controller and VM176 legacy relay cannot both authorize one task. Verify lock ownership and exactly-once intent/launched/terminal markers from fresh, noninterfering observations.
3. Give VM179 an explicit execution contract only after confirming its actual launcher and workspace; the present snapshot does not show one.
4. Require an exclusive GPU lease and current owner check before any later VM176 task. Keep CodexB's independent test authority separate.
5. Keep MIG-0002 at **DESIGN_ONLY**, pending independent GPT Review and a separate immutable authorization. No next task was launched here.
