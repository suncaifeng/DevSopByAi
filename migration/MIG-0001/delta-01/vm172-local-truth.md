# VM172 Local Runtime Truth — MIG-0001 Delta 01

## Classification and observation

- **USER_REPORTED:** VM172 (`10.145.45.72`) is the Codex host and AI Control plane.
- **LIVE_VERIFIED:** The current local host resolves to `ai-control`, owns `10.145.45.72/25`, and is Debian GNU/Linux 13 (trixie), kernel `6.12.107+deb13-amd64`.
- **Observation:** `2026-10-08T08:09:30Z` for the normalized host/runtime transcript; targeted process and systemd checks were repeated between `08:05Z` and `08:09Z`.
- **Executor:** user `debian`. The Codex process and its code-mode child have cwd `/home/debian`; the tool shell started in `/srv/devsop`. The authorized task runs in a separate clean clone at `/tmp/codexc-mig0001-delta01-SLoCNR/repo`.
- **GIT_REPORTED:** The separate task clone is `suncaifeng/DevSopByAi`, branch `tasks/mig-0001-runtime-truth-corrective-delta-01`, initial HEAD `4d1531800199ec7bb80e9034199765f0eb69383a`. The SSH remote in the pre-existing `/srv/devsop` checkout is `git@github.com:suncaifeng/DevSopByAi.git`; the isolated task clone uses the same repository over HTTPS.

## Codex processes and dispatch authority

Codex CLI is installed at `/home/debian/.local/bin/codex`, version `codex-cli 0.155.1`. The wrapper SHA256 is `61b0194f3bb6534439c8d26a3ed57d0805f84b884588b761795323eeb92fcf70`.

At `2026-10-08T08:09:30Z`, three active `codex` processes and their `codex-code-mode` children were visible:

| Codex PID | Child PID | User | Started (UTC) | State / cgroup |
|---:|---:|---|---|---|
| 899139 | 900401 | debian | 2026-09-28 06:16:35 | `Sl+` / `user-1000.slice/session-3.scope` |
| 1347014 | 1351773 | debian | 2026-09-30 02:25:53 | `Sl+` / `user-1000.slice/session-3.scope` |
| 1773695 | 1775288 | debian | 2026-10-02 08:13:46 | `Sl+` / `user-1000.slice/session-3.scope` |

The six processes had cwd `/home/debian`. A narrowly filtered, redacted argv scan found no `MIG-*`, `VM###-*`, or `tasks/...` task identity. No arguments or environment values were retained. These sessions are live Codex activity, but their task ownership and whether any session dispatches work are **UNVERIFIED**.

No system or user systemd service/timer matched the bounded Codex/task/relay/supervisor/holiday/dispatcher/launcher/devops/queue unit-name filter. Explicit probes for `vm172-supervisor.service`, `vm172-codexc-relay-supervisor.service`, and `codex-task-supervisor.service` returned `LoadState=not-found`. No matching marker directories were found under `/run`, `/var/lib`, `/etc/systemd/system`, `/home/debian/worktrees`, or `/home/debian/.local/state` (bounded to depth 3). This is not proof that markers cannot exist elsewhere.

**Finding:** VM172 is the live Codex host and has an available CLI, but the available evidence does not prove it is exercising durable task-dispatch authority. No VM172 supervisor, launcher service, ownership lock, or durable launch marker was found in the inspected scope. Do not infer single-controller status from these absences.

## Git worktrees and branch context

The pre-existing `/srv/devsop` checkout is on `main` at `d51707594fff031cd54eace025b2b2ffff883f85`, with 68 untracked paths. It was not modified or used for task edits. Its visible linked worktrees were:

- `/tmp/devsopbyai-codegraph-ab-arm-a-preflight-20261002`, detached at `37bc219ae4f5989d0bfaf6bfb917ae86108d33e1`;
- `/tmp/devsopbyai-codegraph-ab-index-20261002`, detached at the same SHA;
- `/tmp/devsopbyai-codegraph-controlled-ab-codexb-20261002`, branch `codex/codegraph-controlled-ab-codexb`, HEAD `48b8db0852eae19b24ec9a257d67703b8a048e81`.

No VM172 worktree or local ref matching MIG-0001 Delta 01, holiday relay, supervisor, or launcher was found in that checkout. The task branch was inspected and edited only in the newly created clean isolated clone. The dirty `/srv/devsop` tree and the unrelated CodeGraph worktrees remain untouched.

## Evidence and limits

- Normalized host/process/systemd/worktree transcript SHA256: `4f0daa81a738ee0c96b9beaed386bcd17d264062a95ca221597f3d1468275c15`.
- Checks used: `hostname`, `id`, `uname`, `/etc/os-release`, `ip -brief address`, `codex --version`, process metadata without argv/environment, bounded `systemctl` unit-name queries, marker-directory name queries, and `git worktree list`.
- No service, process, timer, marker, SSH trust, firewall, network, or VM state was changed.
- **UNVERIFIED:** task identity and dispatch role of existing Codex sessions; any supervisor or marker outside the bounded inspected paths; whether VM172 and VM176 have a single fenced controller.
