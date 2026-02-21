# Technical Analysis: Pessoa Jurídica

## 1. Domain Modeling
- **Entities**:
  - `Pessoa` (Base Entity - Shared)
    - Responsibilities: Common identity anchor.
    - Core attributes: `id` (UUID), `data_cadastro`
  - `PessoaJuridica`
    - Responsibilities: Company-specific data.
    - Core attributes: `razao_social`, `nome_fantasia`, `cnpj`
- **Value Objects**: 
  - `CNPJ` (implicitly validated string format)
- **Relationships**: `PessoaJuridica` retains a One-to-One relationship to `Pessoa`.

## 2. Database Modeling
- **Tables**:
  - `pessoa_pessoa` (Created in Task 1)
  - `pessoa_pessoajuridica`:
    - `pessoa_id` (OneToOneField to `pessoa_pessoa`, primary_key=True)
    - `razao_social` (CharField, max_length=255, db_index=True)
    - `nome_fantasia` (CharField, max_length=255, null=True, blank=True, db_index=True)
    - `cnpj` (CharField, max_length=14, unique=True, validators=[validate_cnpj])
- **Constraints**: 
  - `cnpj` unique constraint (stored implicitly as only 14 numeric digits without mask).
  - `razao_social` cannot be blank.
- **Indexes**: Database indexes on `cnpj`, `razao_social`, and `nome_fantasia` for faster search queries.
- **Foreign keys**: `pessoa_pessoajuridica.pessoa_id` -> `pessoa_pessoa.id`.

## 3. Architectural Breakdown
1. **Models**: Create `PessoaJuridica` in `pessoa/models.py`.
2. **Managers**: Create `PessoaJuridicaManager` to abstract querysets.
3. **Services/Helpers**: Create `validate_cnpj` pure function. This helper MUST also sanitize the CNPJ string (strip formatting characters like `.`, `/`, `-`) to enforce the `max_length=14` DB constraint and mathematical rules consistently.
4. **Serializers**: Create `PessoaJuridicaSerializer` to handle incoming and outgoing data flattening. 
5. **Use Cases**: Create `CreatePessoaJuridicaUseCase` and `UpdatePessoaJuridicaUseCase`. Must wrap the dual-model save operations in `django.db.transaction.atomic`. The UseCase receives the raw CNPJ from the API and relies on the Domain Model validation logic to ensure integrity.
6. **Views**: Create `PessoaJuridicaViewSet` (`ModelViewSet`). Override `perform_create` and `perform_update` to inject UseCases instead of default `serializer.save()`.
7. **URLs**: Register `PessoaJuridicaViewSet` to router.
8. **Tests**: Implement tests following `docs/test_standard.md`.

## 4. API Proposal
- **Endpoints**: `/api/pessoas/juridica/` and `/api/pessoas/juridica/{uuid}/`.
- **Request Format (POST/PUT)**:
  ```json
  {
    "razao_social": "Empresa XPTO Ltda",
    "nome_fantasia": "XPTO",
    "cnpj": "12345678000199"
  }
  ```
- **Response Format (201/200)**:
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "razao_social": "Empresa XPTO Ltda",
    "nome_fantasia": "XPTO",
    "cnpj": "12345678000199"
  }
  ```

## 5. Test Strategy
- **Data Generation**: Use `model_bakery.baker.make` for all mock implementations.
- **Unit tests (`django.test.TestCase`)**:
  - Validate CNPJ logic in isolated tests.
  - Test `CreatePessoaJuridicaUseCase` atomic transactional behavior.
- **Integration tests (`rest_framework.test.APITestCase`)**:
  - Test ViewSets using `APIRequestFactory` and `.as_view()`. Ensure 201 statuses and proper error responses for duplicated CNPJs.
- **Edge cases**: Invalid CNPJ lengths, duplicate CNPJ attempts.

## 6. Risks & Tradeoffs
- **Tradeoff**: Overriding `perform_create` in `ModelViewSet` requires the UseCase to return the created instance so that the view can still properly serialize the outgoing response, preserving the DRF ViewSet ecosystem while enforcing Clean Architecture.
