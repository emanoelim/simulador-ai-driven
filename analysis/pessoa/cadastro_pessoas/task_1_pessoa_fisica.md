# Technical Analysis: Pessoa Física

## 1. Domain Modeling
- **Entities**:
  - `Pessoa` (Base Entity)
    - Responsibilities: Common identity anchor for any person type in the system.
    - Core attributes: `id` (UUID), `data_cadastro`
  - `PessoaFisica`
    - Responsibilities: Individual-specific identity and data.
    - Core attributes: `nome_completo`, `cpf`, `data_nascimento`
- **Value Objects**: 
  - `CPF` (implicitly validated string format)
- **Relationships**: `PessoaFisica` has a One-to-One relationship to `Pessoa`.

## 2. Database Modeling
- **Tables**:
  - `pessoa_pessoa`: 
    - `id` (UUIDField, primary_key=True, default=uuid.uuid4, editable=False)
    - `created_at` (DateTimeField, auto_now_add=True)
  - `pessoa_pessoafisica`:
    - `pessoa_id` (OneToOneField to `pessoa_pessoa`, primary_key=True)
    - `nome_completo` (CharField, max_length=255)
    - `cpf` (CharField, max_length=11, unique=True)
    - `data_nascimento` (DateField)
- **Constraints**: 
  - `cpf` unique constraint.
  - `data_nascimento` cannot be in the future (enforced via validators).
- **Indexes**: Database index on `cpf`.
- **Foreign keys**: `pessoa_pessoafisica.pessoa_id` -> `pessoa_pessoa.id`.

## 3. Architectural Breakdown
1. **Models**: Create `Pessoa` and `PessoaFisica` in `pessoa/models.py`. Ensure PK is UUID.
2. **Managers**: Create `PessoaFisicaManager` to abstract querysets.
3. **Services/Helpers**: Create `validate_cpf` and `validate_data_nascimento` pure functions in `pessoa/helpers/validators.py`.
4. **Serializers**: Create `PessoaFisicaSerializer`. It should accept flattened data (nome, cpf, data_nascimento) and validate it.
5. **Use Cases**: Create `CreatePessoaFisicaUseCase` and `UpdatePessoaFisicaUseCase`. Use `django.db.transaction.atomic` to ensure both `Pessoa` and `PessoaFisica` are created/updated synchronously.
6. **Views**: Create `PessoaFisicaViewSet` inheriting from `ModelViewSet`. Override `perform_create` and `perform_update` to delegate execution to the UseCases.
7. **URLs**: Register `PessoaFisicaViewSet` with a DRF router in `pessoa/urls.py`.
8. **Tests**: Implement tests strictly following `docs/test_standard.md`.

## 4. API Proposal
- **Endpoints**: `/api/pessoas/fisica/` and `/api/pessoas/fisica/{uuid}/`.
- **Request Format (POST/PUT)**:
  ```json
  {
    "nome_completo": "João Silva",
    "cpf": "12345678901",
    "data_nascimento": "1990-01-01"
  }
  ```
- **Response Format (201/200)**:
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "nome_completo": "João Silva",
    "cpf": "12345678901",
    "data_nascimento": "1990-01-01"
  }
  ```

## 5. Test Strategy
- **Data Generation**: Use `model_bakery.baker.make` for generating database instances.
- **Unit tests (inherit from `django.test.TestCase`)**:
  - `test_validators.py`: Validate CPF algorithms and future date rejection without HTTP context.
  - `test_use_cases.py`: Validate `transaction.atomic` rollback behavior (e.g., when DB constraints fail) via direct python calls. 
- **Integration tests (inherit from `rest_framework.test.APITestCase`)**:
  - `test_views.py`: Use `APIRequestFactory` and test the ViewSet directly via `as_view()`. Assert 201 Created and correct JSON response including the generated UUID. Verify 400 Bad Request on duplicate CPFs.
- **Edge cases**: Concurrent identical POST requests (should be caught by DB unique constraint).

## 6. Risks & Tradeoffs
- **Tradeoff**: Overriding `perform_create` rather than `create` allows us to still leverage parts of DRF's validation flow in the serializer, while cleanly injecting our UseCase for the actual database orchestration. This perfectly balances DRF's convenience with the project's Clean Architecture goals.
