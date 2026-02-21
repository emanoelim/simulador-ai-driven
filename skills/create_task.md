# Skill: Create Task (PM Mode)

## Objective
Transform a high-level request into a structured product task specification.

Do NOT propose technical implementation.
Do NOT propose database modeling.
Do NOT propose architecture.
Focus only on business requirements.

---

## Required Output Structure

### 1. Business Context
- Why this feature exists
- Business goal

### 2. Scope
- What is included
- What is excluded

### 3. Functional Requirements
List all required behaviors.

Example:
- The system must allow registering Pessoa Física.
- The system must require CPF.
- The system must validate CPF format.

### 4. Required Fields
List business-level fields only.

Example:
- Nome completo
- CPF
- Data de nascimento

(No field types. No DB concerns.)

### 5. Validation Rules (Business-Level)
- CPF must be unique
- Data de nascimento cannot be future date

### 6. Acceptance Criteria
Describe success scenarios in plain language.

---

## Persistence Rule

Save output to:
/tasks/app_name/<feature_name>.md