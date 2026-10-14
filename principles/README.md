# DevSopByAi Core Principles Index

## Purpose

DevSopByAi principles define the engineering boundaries for AI-agent-driven software execution.

The core lifecycle is:

```
TaskContract
      ↓
Git Boundary
      ↓
Agent Execution Verification
      ↓
Execution Evidence
      ↓
Runtime Truth
      ↓
Acceptance Gate
```

---

## Principles

### 1. TaskContract Immutability

Tasks must define scope, constraints, acceptance criteria, and execution boundaries before agent execution.

A running agent task must not silently change its contract.

---

### 2. Git Boundary

Git state is the boundary of engineering truth.

Execution results must be represented through commits, branches, and reviewable diffs.

---

### 3. Agent Execution Verification

Reference:

`agent-execution-verification.md`

Rule:

> Agent execution verification must be branch/commit ancestry based, not commit-message search based.

Agent task completion MUST be verified through Git topology and artifact evidence.

Verification chain:

```
TaskContract baseline SHA
        ↓
Execution branch ancestry
        ↓
Execution HEAD SHA
        ↓
Commit diff scope
        ↓
Artifact / Execution Evidence validation
```

Commit messages are descriptive metadata only and MUST NOT be used as the primary source of truth for execution verification.

The following inference is prohibited:

```
Task keyword not found in commit message
        ↓
Agent did not execute
```

Correct interpretation:

```
Git ancestry proves execution state.
Commit messages provide hints only.
```

---

### 4. Task-Type-Aware Agent Execution Verification

Rule:

> Agent execution verification must be task-type aware. Review tasks are verified by evidence artifacts, not Git mutations.

Verification requirements depend on the declared TaskContract type.

Mutation tasks:

```
TaskContract
      ↓
Execution branch
      ↓
HEAD SHA
      ↓
Git diff
      ↓
Changed artifacts
```

Review tasks:

```
TaskContract
      ↓
Execution context
      ↓
Review scope
      ↓
Evidence report
      ↓
Review conclusion
```

A review-only task MUST NOT be judged incomplete solely because no Git mutation occurred.

A modification task MUST NOT be judged complete solely because a report exists without verifying the expected Git changes.

The expected verification method must match the task deliverable.

---

### 5. Execution Evidence

Agent output must be supported by inspectable evidence, including changed files, commits, runtime records, or generated artifacts.

---

### 6. Runtime Truth

Production and runtime decisions must be based on observed system state, not assumptions from design documents.

---

### 7. Acceptance Gate

Completion requires explicit acceptance criteria validation before advancing to the next phase.
