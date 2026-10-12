# Engineering Decision Challenge — Repository-local Read-first Rule v1.0

**Approved scope:** decision-quality review, not a new technical execution gate. **Date:** 2026-10-12.  
**Source/canonical DevSopByAi mind:** https://github.com/suncaifeng/gpu-compute/blob/521e04cce71d9ac309ab3845cc6ef42405502c87/docs/mind/DevSopByAi/ENGINEERING-DECISION-CHALLENGE-SOP-V1-2026-10-12.md

## Mandatory before work

Before planning or executing a task, read this local file, root `AGENTS.md`, the active frozen TaskContract (when any), and this repository's current truth/spec/decisions as applicable. Read actual Git files; chat memory is not current repository evidence. When a substantial new strategy is requested, the **GPT planner must make the challenge before finalizing a new TaskContract**. The executor reads the policy but **does not override a frozen approved TaskContract**.

## Decision challenge: only for consequential choices

Trigger on: new/replacement frameworks or models, architectural rewrites, migration, production cutover, costly long tests, new major dependencies, scope expansion or diversion from a still-unfinished production objective. For routine fixes, repeat tests, existing authorized tasks and routine personal-log records, reading the policy is sufficient; do not create additional reports or interruptions.

Before endorsing a substantial option, explicitly check:
1. **Outcome:** What user-visible capability and acceptance test matters? Are we confusing technical novelty with the objective?
2. **Baseline:** What is the simplest reproducible already-working solution? If none, prioritize a minimum usable baseline. **A baseline must be truthful, workload-specific and quality-tested**; early screening is not production acceptance.
3. **Opportunity cost:** What completion milestone is displaced by the proposed exploration?
4. **Challenge budget:** What comparative benefit, evidence, bounded exploration budget and objective exit/park rule must a replacement demonstrate?
5. **Safety/rollback:** Can the experiment be isolated? Preserve the approved production baseline, safety boundaries, immutable contracts and ability to revert.

Check **the reverse bias**: baseline-first is not a ban on innovation; if an existing option fails a hard requirement or a limited experiment offers compelling benefit, say so. Performance claims must be compared under equivalent model/quantization/hardware/context/power/protocol; favor Coding/Agent task success over synthetic tok/s when that is the goal.

## Required objection when warranted

Give a brief, visible, early **“⚠️ 工程路线偏离提醒”** before drafting the task: summarize goal, existing baseline and uncertainty, opportunity cost, a preferred order or smaller experiment, and a measurable stopping/exit condition. Make a recommendation: `GO`, `GO_WITH_LIMIT`, or `ADVISE_DEFER`. This **advice is not a veto**; user has final strategic authority. `STOP_SCOPE_CONFLICT` applies only to genuine safety/authorization/frozen-contract conflicts.

In substantial proposals or new TaskContract Layer A, include a compact `DECISION_CHALLENGE` record: goal, baseline evidence, competing option, opportunity cost, trial acceptance/exit, advice, user decision. Record `UNKNOWN` rather than invent facts. No record required for routine tasks.

## Role separation and no retroactive gate

**GPT planner/reviewer:** criticizes strategic path before TaskContract freeze and audits outcomes afterwards. **Codex/agy executor:** reads this file before execution, follows the authorized frozen task, logs a witnessed `STRATEGY_RISK` and proposes follow-up if needed; does not silently replan, change tests, abort legitimate work for preference reasons, or self-approve merge. **User:** final strategic choice and existing production/merge approval.

This rule is Git-only, not a service, Supervisor, AI Memory, remote blocking hook, or new safety fuse. It neither unfreezes DevSopByAi nor modifies established `KM-001`, historical evidence, training plans, or any other project SSOT. Repo docs are **not automatically loaded by ChatGPT**; whoever proposes/executes must actually read them.

---

## 2026-10-12 addition — Smallest verifiable MVP closure before polish

**Outcome first, then optimize.** Before proposing a major framework comparison, UI/architecture expansion, migration or long benchmark, identify the **smallest end-to-end user-visible artifact or successful real transaction** the current task can finish and demonstrate. Ship that reproducibly and independently verify it before broadening the work. Pure implementation progress, PRs, “model loaded” and synthetic scores are **not** equivalent to an accepted MVP.

The VM176/VM76 scope is **three independent project domains**, not one monolithic release: [gpu-compute](https://github.com/suncaifeng/gpu-compute) owns GPU control and shared V100 arbitration; [llm-inference](https://github.com/suncaifeng/llm-inference) owns local LLM serving / Coding Agent; [video-generation](https://github.com/suncaifeng/video-generation) owns H3/LTX/ComfyUI video creation. Original [comfyui-minimax-h3](https://github.com/suncaifeng/comfyui-minimax-h3) is historical source; [DevSopByAi](https://github.com/suncaifeng/DevSopByAi) is reserved/frozen. **Do not let one domain wait for the others to complete all feature upgrades**; only the real minimal interface and existing authorized GPU-owner rules are shared.

**Read the current cross-project MVP mind** before planning or executing VM176-related tasks: [VM176 Three-Project Minimum MVP Closure](https://github.com/suncaifeng/gpu-compute/blob/c04a5bda11b8dad8914e1b058bec45d3b72c5a58/docs/mind/DevSopByAi/VM176-THREE-PROJECT-MVP-CLOSURE-2026-10-12.md). In a new strategic proposal identify `MVP_OUTPUT` (artifact/transaction), `MINIMUM_ACCEPTANCE` (real end-to-end proof), `EXCLUDE_UNTIL_LATER` (optional optimization), and `DEPENDENCY_MINIMUM` (only needed cross-project contract); record `UNKNOWN` where no evidence exists. **For routine tasks and already approved frozen tasks, this is not a new gate or a license to alter the contract.** Any mismatch is advice/evidence for a subsequent task, not a reason to self-stop authorized work.

**MVP means minimal scope, not lower security, hardware safety, quality or review standards.**
