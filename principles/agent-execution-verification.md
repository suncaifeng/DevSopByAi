# Agent Execution Verification Principle

## Core Principle

Agent execution verification must be branch/commit ancestry based, not commit-message search based.

Agent task completion MUST be verified from Git state transitions:

```
TaskContract baseline SHA
        ↓
Execution branch ancestry
        ↓
Execution HEAD SHA
        ↓
Commit diff scope
        ↓
Artifact / evidence validation
```

Commit messages are descriptive metadata only. They MUST NOT be used as the primary source of truth for execution verification.

A missing task keyword in commit messages does NOT imply task non-execution.

Git history topology is the source of truth; commit naming is not.

---

## Verification Procedure

For every Codex / agy / Agent execution:

1. Identify the execution branch.
2. Resolve branch HEAD SHA and commit ancestry.
3. Compare baseline SHA from TaskContract with execution SHA.
4. Inspect changed files and diff scope.
5. Validate execution evidence and acceptance criteria.

The verification order is:

```
Git topology
    ↓
Commit ancestry
    ↓
Diff scope
    ↓
Artifact validation
    ↓
Runtime evidence
```

---

## Anti-patterns

### Commit Message Verification

Incorrect:

```
Search commit messages for TaskContract ID.

No matching commit found.

Conclusion: Agent did not execute.
```

Why incorrect:

- Agents may use descriptive commit messages.
- Squash, rebase, or manual commit naming may change messages.
- Commit messages describe changes but do not establish execution lineage.

Correct:

```
TaskContract baseline SHA
        ↓
Execution branch
        ↓
HEAD ancestry
        ↓
Diff inspection
        ↓
Evidence review
```

---

## Required Verification Metadata

Agent execution reviews SHOULD include:

```yaml
verification_method:
  type: git_ancestry_based

commit_message_search:
  allowed_as_hint_only: true

branch_head_verified:
  required: true

diff_scope_verified:
  required: true

evidence_verified:
  required: true
```

---

## Relationship With DevSopByAi Architecture

This principle extends the existing execution model:

```
TaskContract
      ↓
Git Boundary
      ↓
Agent Execution Verification
      ↓
Runtime Truth
      ↓
Acceptance Evidence
```

The purpose is to ensure that autonomous agent workflows remain reproducible, auditable, and independent from human-readable commit naming conventions.
