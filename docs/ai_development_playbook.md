# AI Development Playbook

This document defines how AI-assisted development must be conducted in this project.

It ensures consistency, architectural integrity, and reproducibility.

---

# 1. Overview

This project uses a structured AI-driven workflow composed of four stages:

1. create_task (Product Level)
2. technical_analysis (Engineering Level)
3. architectural_review (Audit Level)
4. execute_task (Implementation Level)

Each stage must be executed in order.

## 1.1 Roles Mapping

| Stage                | Role Equivalent |
|----------------------|----------------|
| create_task          | Product / PM   |
| technical_analysis   | Senior Dev     |
| architectural_review | Architect      |
| execute_task         | Developer      |

---

# 2. Workflow Diagram

Product → Technical → Review → Execute

No phase may be skipped.

---

# 3. Skill Definitions

## 3.1 create_task

Purpose:
- Define business requirements.
- Written in PM language.
- No technical decisions allowed.

Output location:
- /tasks/

Must include:
- Business context
- Scope
- Functional requirements
- Required fields
- Acceptance criteria

---

## 3.2 technical_analysis

Purpose:
- Convert business task into technical plan.
- Define domain modeling, DB, API, tests.

Output location:
- /analysis/

Must:
- Respect architectural_standard.md
- Respect testing_standards.md
- Confirm stack usage

---

## 3.3 architectural_review

Purpose:
- Audit technical_analysis before implementation.

Must:
- Detect violations
- Classify severity
- Suggest improvements
- Not modify files

---

## 3.4 execute_task

Purpose:
- Implement incrementally.

Rules:
- One phase at a time
- Suggest next phase automatically
- Wait for approval
- Respect all standards

---

# 5. Governance Rules

- No direct implementation without technical_analysis.
- No implementation without architectural_review.
- No skipping phases.
- No silent stack changes.
- No silent dependency additions.

---

# 6. How To Add New Skills

New skills must:
- Be documented here
- Define objective
- Define constraints
- Define output format
- Define when to use