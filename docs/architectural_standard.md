# Architectural Standard

## Objective

Define the mandatory architectural pattern for all modules in the project.

All new features and refactorings must strictly follow this standard.

---

# Module Structure

Each Django app/module must follow this structure:

projeto/ 
├── projeto/ 
│ ├── app_1/ 
│ │ ├── tests/
│ │ │ ├── api/ 
│ │ │ │ ├── test_method_app_1.py 
│ │ │ ├── use_cases/ 
│ │ │ │ ├── test_use_case_app_1.py 
│ │ │ ├── services/ 
│ │ │ │ ├──  test_service_app_1.py 
│ │ ├── use_cases/ 
│ │ │ ├── use_case_app_1.py 
│ │ ├── services/ 
│ │ │ ├── app_1_domain_service.py 
│ │ ├── helpers/ 
│ │ │ ├── app_1_domain_helper.py
│ │ ├── admin.py 
│ │ ├── apps.py 
│ │ ├── urls.py 
│ │ ├── views.py 
│ │ ├── serializers.py 
│ │ ├── permissions.py 
│ │ ├── filters.py 
│ │ ├── exceptions.py
│ │ ├── models.py 
│ │ ├── receivers.py 
│ ├── infra/ 
│ │ ├── services 
│ │ │ ├── external_service_1.py 


---

# Layer Responsibilities

## Views

- Responsible only for HTTP handling.
- Must not contain business logic.
- May call UseCases.
- Must not perform complex queries.
- Should not access the database directly.
- Should not orchestrate business rules.

---

## Serializers

- Responsible for:
  - Data validation
  - Data transformation (JSON ↔ object)
- Must not contain business logic.
- Must not perform complex queries.
- Must not orchestrate domain actions.
- May call Managers for validation-related queries only.

---

## UseCases

- Represent a complete system action.
- Encapsulate a business flow.
- Orchestrate execution.
- May call:
  - DomainServices
  - Managers
  - Models
- Must not depend on HTTP layer.
- Must not call other UseCases.
- Should be deterministic and testable in isolation.

---

## DomainServices

- Contain reusable business rules.
- Do not represent full system actions.
- May access Models.
- Must not depend on HTTP layer.
- Must not contain orchestration logic.
- Should not manage transactions directly.

---

## Models

- Represent a single database row.
- Responsible for:
  - Data structure
  - Internal consistency
- Must not:
  - Create other model instances
  - Contain complex business rules
  - Orchestrate domain flows
- May delegate logic to DomainServices.
- May access related models.

---

## Managers

- Responsible for:
  - Object creation
  - Query abstraction
- Encapsulate database access logic.
- Must not contain business rules.
- Should expose intention-revealing query methods.

Examples:
- `get_active_plans()`
- `get_pending_documents()`

---

## Helpers

- Contain simple utility functions.
- Must be pure whenever possible.
- Must not access the database.
- Must not contain business rules.

---

# Dependency Rules

Allowed dependencies:

- View → UseCase
- Serializer → Manager (validation only)
- UseCase → DomainService / Manager / Model
- DomainService → Model
- Model → DomainService (delegation only)

Forbidden dependencies:

- UseCase → View
- Model → View
- Model → UseCase
- Manager → UseCase
- Helper → Database access

---

# Explicit Prohibitions

The following are not allowed:

- Business logic inside Views
- Complex queries inside Serializers
- Object creation inside Models
- UseCase calling another UseCase
- Cross-module hidden dependencies
- Business rules inside Managers
- HTTP-aware logic outside Views

---

# Testing Guidelines

- Each layer must have isolated tests.
- UseCases must be testable without HTTP.
- DomainServices must be testable without serializers.
- Views should be tested via API tests only.

---

# General Principles

- Prefer explicit over implicit.
- Favor composition over inheritance.
- Keep business rules centralized.
- Keep HTTP concerns isolated.
- Refactor incrementally.
- Preserve behavior during refactorings.

---

# API Layer Standards

- Prefer ModelViewSet unless strong reason not to.
- Prefer overriding perform_create over create in ModelViewSet.
