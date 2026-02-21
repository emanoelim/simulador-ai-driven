# Testing Standards

This document defines mandatory testing rules for the project.

All technical analysis and implementation must strictly follow these standards.

---

# 1. Testing Philosophy

- Tests must validate behavior, not implementation details.
- Business rules must be tested independently of the HTTP layer.
- Transactional behavior must be validated using real database operations.
- Tests must reflect real-world usage scenarios.
- No silent mocking of core infrastructure.

---

# 2. Test Stack Definition

## 2.1 Base Test Class

- API tests must inherit from:
  - `rest_framework.test.APITestCase`

- Domain and UseCase tests may inherit from:
  - `django.test.TestCase`

- Do NOT use pytest unless explicitly approved.

---

## 2.2 Request Tools

- For endpoint testing, use:
  - `APIRequestFactory`

- Prefer testing ViewSets directly using `as_view()` when isolation is required.
- Avoid over-reliance on APIClient unless full integration behavior is desired.

---

## 2.3 Data Creation

- Use **Model Bakery** for test data generation.

--- 

# 3. Coverage

All UseCases must have:
- At least one success test
- At least one failure test