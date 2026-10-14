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

### 4. Execution Evidence

Agent output must be supported by inspectable evidence, including changed files, commits, runtime records, or generated artifacts.

---

### 5. Runtime Truth

Production and runtime decisions must be based on observed system state, not assumptions from design documents.

---

### 6. Acceptance Gate

Completion requires explicit acceptance criteria validation before advancing to the next phase.
