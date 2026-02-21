# Feature: Cadastro de Pessoas (Física e Jurídica)

### 1. Business Context
- **Why this feature exists**: O sistema precisa de um cadastro básico para identificar indivíduos (Pessoa Física) e empresas/organizações (Pessoa Jurídica) com as quais irá interagir.
- **Business goal**: Garantir o registro, identificação única e a precisão dos dados das pessoas cadastradas na plataforma.

### 2. Scope
- **What is included**:
  - Cadastro, leitura, atualização e exclusão (CRUD) de Pessoa Física.
  - Cadastro, leitura, atualização e exclusão (CRUD) de Pessoa Jurídica.
- **What is excluded**:
  - Dados de contato (e-mail, telefone), pois deverão fazer parte de um módulo de contatos ou relacionamentos futuros.
  - Endereços físicos e dados de faturamento/pagamento.

### 3. Functional Requirements
- O sistema deve permitir o cadastro de Pessoa Física.
- O sistema deve permitir o cadastro de Pessoa Jurídica.
- O sistema deve exigir CPF para cadastro de Pessoa Física.
- O sistema deve exigir CNPJ para cadastro de Pessoa Jurídica.
- O sistema não deve exigir dados de contato para a conclusão do registro.
- O sistema deve validar a autenticidade e formatação de CPFs.
- O sistema deve validar a autenticidade e formatação de CNPJs.
- O sistema deve permitir a alteração e atualização dos dados (exceto o número do documento principal em uso).
- O sistema não deve permitir o cadastro do mesmo documento mais de uma vez.

### 4. Required Fields

**Pessoa Física**
- Nome completo
- CPF
- Data de nascimento

**Pessoa Jurídica**
- Razão social
- Nome fantasia
- CNPJ

### 5. Validation Rules (Business-Level)
- O CPF precisa ser válido matematicamente e único na base do sistema.
- O CNPJ precisa ser válido matematicamente e único na base do sistema.
- A Data de nascimento não pode estar no futuro ou representar uma idade inválida/impossível (superior a 120 anos).
- Razão social e Nome completo são campos obrigatórios e não podem estar em branco.

### 6. Acceptance Criteria
- Como um operador, quando eu cadastro um indivíduo com um CPF e nome válidos, então o sistema deve salvar o registro com sucesso e confirmá-lo.
- Como um operador, quando eu tento cadastrar uma pessoa física contendo um CPF já registrado em outro cadastro, o sistema deve recusar a tentativa e informar sobre a duplicidade do documento.
- Como um operador, quando eu cadastro uma empresa com Razão Social preenchida e um CNPJ válido, então o sistema deve concluir a ação com sucesso.
- Como um operador, quando eu insiro um CNPJ com formato irregular ou dígitos inválidos, o sistema deve impedir o registro e reportar "CNPJ inválido".
- Como um operador, quando tento registrar uma Data de nascimento no futuro para uma Pessoa Física, a ação deve ser bloqueada.

### 7. Non-Functional Requirements
- O sistema deve garantir integridade dos dados.
- O sistema deve impedir inconsistências em operações concorrentes.