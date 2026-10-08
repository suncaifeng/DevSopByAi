# Runtime Truth — read-only observations

Audit date: 2026-10-08 UTC. Host inspection was read-only. No service, process, timer, firewall, GPU, model, or VM configuration was changed. The source reports below are Git assertions; they do not replace the live observations.

## VM172 — 10.145.45.72

**UNVERIFIED.** From VM176 at 2026-10-08T07:25:55Z, non-interactive SSH failed with `Host key verification failed` (exit 255). No host key was added, no verification option was weakened, and no host data was collected. VM172 supervisor state, active services, checkouts, GPU, lease, and durable markers therefore remain unknown. `vm172-supervisor.service` being absent on VM176 is not evidence about VM172.

## VM176 — 10.145.45.76 (`compute`)

Observed at 2026-10-08T07:21:19Z: Debian GNU/Linux 13 (trixie), kernel `6.12.107+deb13-amd64`.

| Assertion | Classification | Observation |
|---|---|---|
| `ai-comfyui.service` | LIVE_VERIFIED | loaded, active/running, user `debian`, working directory `/opt/ai/runtimes/comfyui`, ExecStart `/opt/ai/runtimes/comfyui/start.sh`; listener `0.0.0.0:8188`; local `/system_stats` returned HTTP 200. |
| ComfyUI process | LIVE_VERIFIED | PID 166059, executable `/opt/ai/venvs/comfyui-track-a/bin/python`, cwd `/opt/ai/runtimes/comfyui`; the only compute process listed by `nvidia-smi`. No process action was taken. |
| Live ComfyUI Git checkout | CONFLICT (provenance only) | `/opt/ai/runtimes/comfyui` is detached at `c2bcbecd82ec5ae66594340b395c24ef0217b238` (`ComfyUI v0.32.0`, 2026-08-11); `start.sh` is untracked. This commit is not an advertised H3 repository head and its source lineage could not be established from the audited H3 refs. This is a provenance conflict, not a claim that the running service is unhealthy. |
| GPU | LIVE_VERIFIED | Tesla PG500-216 / GV100, UUID `GPU-dc79284d-eaf5-86cb-ab69-f1d13a84c6c8`, BDF `00000000:01:00.0`, driver 580.105.08; 30 C, 35.63/250 W, 32768 MiB total / 27596 MiB used, uncorrected volatile and aggregate ECC both 0. PID 166059 used 27570 MiB. |
| Root filesystem | LIVE_VERIFIED | `/dev/sda1`, ext4, 251.8G total, 107.4G available, 53% used. |
| Selected kernel fault search | LIVE_VERIFIED, bounded | Filtered kernel journal since 2026-10-02 for Xid, uncorrected ECC, OOM, or Oops returned no matching lines. This does not establish absence outside the retained journal or filter. |
| `vm176-holiday-relay.service` | LIVE_VERIFIED | loaded, disabled, inactive/dead. ExecStart points at `/home/debian/worktrees/comfyui-minimax-h3-codexc-relay-supervisor/ops/vm176-holiday-relay/supervisor.py --daemon`. Unit SHA256 `90e59820441490d7438b2370da917c4af501d945e0df8248c40de44f261c5d53`; launcher config SHA256 `82980faf0cabdec57155b03f063176dee64f271d28f2165dadfd51c2ba4a18a8`; supervisor script SHA256 `82945e5412960f5ce70f98b8a0c6643543bebb4bebd5dbff173db5629142aedb`. Source worktree is branch `codex/holiday-relay-supervisor-codec`, HEAD `afe6311af8586336ef240a14fc4395569547d57e`. |
| Relay durable state | LIVE_VERIFIED | `/var/lib/vm176-holiday-relay` exists, mode 0750, owned by debian. `state.json`, `source-terminal.json`, `live-gate.json`, `supervisor.log`, and `supervisor.lock` exist. `codexb.launch.intent` and `codexb.launched` are absent. Only status/reason fields were read: launcher status `BLOCKED` because no Codex CLI path was available; state result `DRY_RUN_READY`, `launch_suppressed=true`, source result `BLOCKED`, updated `2026-10-02T09:17:05Z`. The persistent lock file is not evidence of a live lock owner. |
| `ai-llm`, `h3-story-console`, `h3-video-stack`, `comfyui-h3`, `vm172-supervisor` units | LIVE_VERIFIED as absent on this host only | `LoadState=not-found`; this does not establish service state on another VM. |
| Live GPU lease marker outside relay state | UNVERIFIED | No separate lease path could be established safely from the bounded inspection. The existing ComfyUI GPU owner is visible; no lease marker was inferred from process ownership. |

A separate H3 read-only thermal preflight report, committed at H3 branch head `b3911fa5c6fd1c4597a6c08a9c85d57afd2bed59`, reports 15 one-second samples at 2026-10-08T07:28:07–07:28:21Z: 31–32 C memory/HBM, 30 C core, 35.61–35.72 W draw, 0% utilization and a configured 250 W cap. It reports `BLOCKED` before any cap change or H3/LLM workload because the required baseline was 180 W and no exclusive lease existed. This is **GIT_REPORTED** evidence from that task; no sustained thermal boundary was tested.

A second read-only VM176 check at 2026-10-08T07:34:02Z confirmed `ai-comfyui.service` active/running, VM176 relay disabled/inactive, GPU power limit 250.00 W, draw 35.61 W, 30 C core temperature, 27596 MiB used, the same PID 166059 owner, HTTP 200 on 8188, and both CodexB launch markers absent. This agrees with the separate V100 thermal-task report that its pre-existing cap was 250 W; that report says its own worker did not alter the cap or start a workload.

The running `ai-comfyui` service is the only observed listener among the inspected Git-reported ports. `8188` answered. Ports `8190` (H3 Story), `8191` (LLM control console), and `8080` (Qwen service) had no listener at the observation time. These port purposes are **GIT_REPORTED** by `scripts/h3_story_server.py` and `ops/llm-control-console/*`, not live services. The VM176 H3 runtime is live on `/opt/ai`; historical reports reference other paths, including `/home/debian/ai-models/comfyui` and `/data/ai-models/llm`. Model files were not read or copied.

## VM179 — 10.145.45.79

**UNVERIFIED.** From VM176 at 2026-10-08T07:25:55Z, non-interactive SSH returned `No route to host` (exit 255). No retry route or network setting was changed. VM179 is therefore not established as an execution host in current Runtime Truth.

## Controller safety conclusion

VM176's legacy supervisor is disabled/inactive and has no CodexB intent/launched marker. The VM172 supervisor cannot be observed because VM172 is UNVERIFIED. Therefore the audit cannot rule out a second controller or establish single-controller fencing. Treat dual-authority prevention as an OPEN BLOCKER: keep the relay unarmed, do not launch CodexB, and require independent, read-only verification of both controllers and persistent markers before any separately authorized future task.

VM173 RAG and VM177 storage appear in historical PVE/storage documents on Git refs only. They were not accessed, and no live dependency or health claim is made.
