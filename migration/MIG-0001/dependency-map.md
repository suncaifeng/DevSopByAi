# Cross-repository dependency map and ownership boundaries

This is a proposed four-repository boundary map only. No repositories were created and no files were moved. File/blob-level recommendations, source refs, commits, hashes, and observed refs are in `ownership-proposal.csv` (714 unique path/blob versions).

## Proposed ownership

| Proposed repository | Primary responsibility | Current evidence/source |
|---|---|---|
| `suncaifeng/DevSopByAi` | Control plane, immutable TaskContracts, task/review status, SOP, provenance and migration coordination; development execution is assigned to VM179 by the TaskContract. | Current repository: `main` `e3c609f5cdbe38bca7e17b87359f29817d91237b`; CodeGraph branch `48b8db0852eae19b24ec9a257d67703b8a048e81`. |
| `suncaifeng/gpu-compute` | VM176 hardware lifecycle, GPU lease/fencing, profile/thermal/resource gates, privileged service lifecycle and exclusive execution coordination. | Currently mixed into H3 `ops/`, `systemd/`, runtime scripts and the Holiday Relay; not a clean standalone boundary. |
| `suncaifeng/llm-inference` | LLM engines, Qwen38/OneCat/llama.cpp/NInfer adapters, tokenizer/request proof, C64/C128/C256 harness, benchmark policy, corpora and fixtures. | H3 `benchmarks/vm176-qwen38/`, `ops/llm-control-console/`, `systemd/ai-llm.service`, and runtime helper scripts. |
| `suncaifeng/video-generation` | ComfyUI, H3/LTX workflows, Story server, Director Console, video stack services and media artifact contracts. | H3 `workflows/`, `scripts/h3_story_server.py`, `scripts/director_console_v2/`, and video-specific systemd units. |

The three proposed targets returned public GitHub API HTTP 404 during the earlier read-only check. This cannot distinguish nonexistent from private/inaccessible. The TaskContract's assumption that they do not exist remains unverified; no create attempt was made.

## Dependency graph

```text
DevSopByAi control plane
  ├── immutable TaskContracts, source commit/blob identities, reviews and gates
  ├── authorizes a GPU lease request ───────────────► gpu-compute (VM176)
  ├── authorizes LLM execution task ────────────────► llm-inference
  └── authorizes generation task ───────────────────► video-generation

gpu-compute (single fenced VM176 owner)
  ├── grants/revokes a lease and publishes health/thermal/resource snapshot
  ├── gates llm-inference process launch
  └── gates video-generation process launch

llm-inference ◄── health/control console ──► video-generation
  Qwen endpoints 8080; console 8191; H3 Story 8190; ComfyUI API 8188
```

The last four port numbers are **GIT_REPORTED**: `scripts/h3_story_server.py` binds 8190 and defaults to ComfyUI `127.0.0.1:8188`; `ops/llm-control-console` documents 8191 and probes 8080/8190/8188. At 2026-10-08T07:21:19Z only 8188 was listening and healthy on VM176. Do not treat the other ports as live.

## Contracts required before any later split

1. **Task/evidence contract:** DevSopByAi owns immutable task identity, allowed writes, source/target commits, content hashes, status vocabulary, independent Review result, and next gate. A launch prompt or copied task file cannot supersede a Git TaskContract.
2. **GPU lease/fencing:** gpu-compute is the only privileged GPU lifecycle owner. Lease records need a unique owner, VM identity, expiry/heartbeat, monotonic fencing token, exact process/unit identity, and durable idempotent release. LLM/video services must not independently reset, kill, reconfigure, or start the GPU.
3. **LLM request identity:** llm-inference publishes exact model/revision/hash, tokenizer/input hash, raw request/response proof, route identity, runtime version and normalized metrics. Policy versions remain immutable and task-specific.
4. **Video execution identity:** video-generation publishes workflow hash, model/asset metadata, route, dimensions/frame count, output SHA, technical QC and human approval separately. `review_pending` is not production acceptance.
5. **Readiness API:** console/UI health checks consume narrow read-only status endpoints; no generic command execution, lease creation, model loading or start/stop privilege crosses the service boundary.
6. **Archive provenance:** TaskContracts, terminal reports, manifests, runtime evidence and rollback references remain addressable by original repository/ref/commit/blob. The archive mapping is not a physical migration performed here.

## Source paths, ports, environment and assets

- H3 main is `644d7ff2a7a00e04db94ab347a85ed61488d5a76`. It tracks `systemd/ai-comfyui.service`, `systemd/ai-llm.service`, `systemd/comfyui-h3.service`, `systemd/h3-story-console.service`, and `systemd/h3-video-stack.service`; most legacy unit locations reported in files differ from VM176's current `/opt/ai/runtimes/comfyui` deployment.
- Git examples include `config/gpu.env.example` and `config/comfyui/extra_model_paths.yaml.example`. Git-reported environment file paths include `/opt/ai/config/gpu.env` and `/opt/ai/config/llm/runtime.env`; live secret contents were not inspected.
- Static code/config scans of the audited main and relevant corrective branches did not find literal `10.145.45.72`, `.76`, `.79`, `.173` or `.177` addresses in selected executable/config roots. They did find VM-specific runtime/model paths and several `comfyui-minimax-h3` references; search scope is listed in the risk register.
- H3 main has no tracked `models/` directory or model payloads. Historical reports contain model repository, revision, file-hash and destination metadata. Treat model payloads as external and do not copy them as part of a repository split.
- VM173 RAG and VM177 storage appear in PVE/storage plans and task documents only. Their live services, mounts and health were not inspected.

## DevSop SOP and CodeGraph experiment

`开发SOP流程与提示词.md` records a pipeline from user task through GPT semantic specification, strict DSL compilation, Gemini adversarial review, GPT repair/final validation, and Codex execution. The Git TaskContract remains the immutable execution authority for this audit. The CodeGraph A/B report on the `codex/codegraph-controlled-ab-codexb` branch self-reports COMPLETE while awaiting independent GPT review and explicitly says `ENGINEERING_DISPOSITION: DO_NOT_ADOPT`. Its 16 measured runs and four internal blinded validators found Arm B missed critical `can_retry_codex` and `can_repair_spec` fields in Q1-R2-B; recall was A 74/86 vs B 73/86 and B's measured medians were worse. The experiment therefore does not authorize adoption. The CodeC TaskContract has no matching terminal report.

## Ownership proposal semantics

`KEEP` means the proposed target remains the domain owner after a separate migration task. `SPLIT_REQUIRED` means isolate privileged lifecycle from application behavior behind a versioned interface before migration. `ARCHIVE_ONLY` means preserve contracts/evidence and provenance in the control-plane archive; it does not instruct a copy now. Every row contains source repository, ref, head commit, path, Git blob SHA and observed refs. Both Task 2.1 contract blob variants are represented separately.
