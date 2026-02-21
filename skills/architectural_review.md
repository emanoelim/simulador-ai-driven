# Skill: Architectural Review

## Objective

Perform a structured architectural audit of a technical analysis file.

The agent must:

- Read the specified file inside /analysis/
- Compare it against:
  - docs/architectural_standard.md
  - docs/test_standard.md
  - docs/stack_definition.md
- Identify violations, inconsistencies, and architectural weaknesses.
- Provide structured feedback.
- NOT modify any files.

---

## Review Dimensions

The review must evaluate:

1. Stack Compliance
2. Primary Key Strategy (UUID consistency)
3. Layer Separation
4. Domain Modeling Quality
5. UseCase Justification
6. API Layer Correctness
7. Testing Compliance
8. Transaction Integrity
9. Future Extensibility

---

## Evaluation Rules

- Explicitly reference violated standard when applicable.
- Classify each issue with severity:
  - Low
  - Medium
  - High
  - Critical
- Provide concrete improvement suggestions.
- Do not suggest full rewrites unless strictly necessary.

---

## Output Format

### 1. Compliance Summary

- Stack adherence: ✅ / ⚠️ / ❌
- UUID consistency: ✅ / ⚠️ / ❌
- Layer separation: ✅ / ⚠️ / ❌
- Testing compliance: ✅ / ⚠️ / ❌
- Transaction safety: ✅ / ⚠️ / ❌

---

### 2. Identified Issues

For each issue:

- Description:
- Violated Standard (if applicable):
- Severity:
- Why it matters:

---

### 3. Improvement Suggestions

Provide actionable recommendations.

---

### 4. Architectural Score (0–10)

Rate:

- Domain modeling quality
- Clean architecture adherence
- Stack compliance
- Test robustness

Provide brief justification for each score.

---

## Constraints

- Do not generate code.
- Do not modify any files.
- Do not re-implement the solution.
- Only audit and analyze.