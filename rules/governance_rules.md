# AI Governance Rules

This document defines mandatory behavioral rules for all AI-assisted development in this project.

These rules override all skills and instructions.

Non-compliance is not allowed.

---

# 1. Workflow Enforcement (Hard Rule)

No feature implementation may begin unless the following artifacts exist:

1. A business task in /tasks/
2. A technical analysis in /analysis/
3. An architectural review of the technical analysis

If any of these are missing, the AI must:

- Refuse implementation
- Explain which step is missing
- Suggest the correct next step

Direct implementation without workflow compliance is forbidden.

---

# 2. No Direct Coding Rule

If the user asks to:

- "Implement X"
- "Create the model"
- "Just code it"
- "Generate the full solution"

The AI must:

1. Check for workflow compliance.
2. If missing phases, refuse execution.
3. Redirect to the appropriate skill:
   - create_task
   - technical_analysis
   - architectural_review
   - execute_task

The AI must never bypass the structured workflow.

---

# 3. Skill Invocation Requirement

All development actions must be triggered explicitly using skills.

Valid patterns:

- Apply create_task for <feature>
- Apply technical_analysis for <task>
- Apply architectural_review for <analysis>
- Apply execute_task for <analysis>

Free-form implementation requests must not be executed.

---

# 4. Architecture Protection Rules

The AI must never:

- Change primary key strategy (UUID)
- Replace required libraries (e.g., model_bakery)
- Introduce new dependencies silently
- Move business logic into Views or Serializers
- Mock Django ORM for transactional tests

If a requested change violates architectural standards,
the AI must explicitly warn and request approval.

---

# 5. Incremental Execution Rule

Implementation must:

- Occur one phase at a time
- Follow dependency order
- Suggest next logical phase
- Wait for explicit user approval before applying changes

Bulk or full-module generation is forbidden.

---

# 6. Dependency Governance

If new dependencies are required:

The AI must:

1. Explicitly state why the dependency is required.
2. Propose adding it to requirements.
3. Wait for approval.

Silent dependency introduction is forbidden.

---

# 7. Test Enforcement Rule

Every implemented UseCase must include:

- At least one success test
- At least one failure test

Every API endpoint must include:

- At least one success test
- At least one validation failure test

Tests must follow docs/testing_standards.md.

---

# 8. Refusal Policy

If a request violates any governance rule,
the AI must:

- Refuse execution
- Clearly explain the violation
- Suggest the correct compliant action

Compliance with governance rules is mandatory.