# Skill: Execute Task

## Objective

Implement a previously approved technical analysis task in a controlled, incremental, and architecture-compliant manner.

The agent must:

- Read the corresponding file inside /analysis/
- Respect docs/architectural_standard.md
- Respect docs/testing_standards.md
- Respect docs/stack_definition.md (if present)
- Follow project-wide architectural constraints

---

## Phase Selection Rule

The agent must:

1. Read the architectural breakdown inside the analysis file.
2. Inspect the current project structure.
3. Detect which phases are already implemented.
4. Determine the correct next pending phase.
5. Propose the next logical phase based on dependency order.
6. Explain why this phase must be implemented next.
7. Wait for explicit user approval before proceeding.

If the user explicitly specifies a phase, validate dependency order before executing.

---

## Execution Rules

1. Never implement everything at once.
2. Execute only one architectural layer per cycle.
3. Always suggest the next logical phase automatically.
4. Show a structured execution plan before proposing code.
5. The agent must not create, modify, or apply any file before explicit user approval.
6. If partial implementation exists, continue incrementally.
7. Never silently change stack, dependencies, or architectural patterns.

---

## Valid Execution Phases

- domain
- models
- repositories
- use_cases
- api
- tests

Phases must respect dependency order:

domain → models → repositories → use_cases → api → tests

---

## Implementation Constraints

- UUID must be used as defined in architectural standards.
- No business logic inside serializers or views.
- Views must delegate business logic to UseCases.
- Prefer overriding `perform_create` and `perform_update` instead of `create`.
- Tests must follow docs/testing_standards.md strictly.
- Use `model_bakery` for test data generation.
- Do not mock Django ORM for transactional behavior.
- Transactional integrity must use `django.db.transaction.atomic`.

---

## Output Format

### 1. Phase Status

Indicate detected status:

- domain: pending / completed
- models: pending / completed
- repositories: pending / completed
- use_cases: pending / completed
- api: pending / completed
- tests: pending / completed

---

### 2. Phase Suggestion

- Proposed next phase:
- Justification:

---

### 3. Execution Plan

List:

- Files to be created
- Files to be modified
- Dependencies involved
- Tests to be added (if applicable)

No code yet in this section.

---

### 4. Proposed Changes (After Approval Only)

Show:

- File content or diffs
- Clear separation per file
- No hidden modifications

---

### 5. Await Approval

The agent must explicitly wait for user confirmation before applying any changes.