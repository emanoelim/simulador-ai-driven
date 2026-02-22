# Feature: Cadastro de Contatos (Pessoa Física e Jurídica)

### 1. Business Context
- **Why this feature exists**: Após viabilizar o cadastro base de pessoas (físicas e jurídicas), o sistema precisa permitir o armazenamento estruturado de meios de comunicação para permitir interações diretas.
- **Business goal**: Garantir que as pessoas cadastradas na plataforma possuam múltiplos pontos de contato organizados por título/categoria para uso futuro em comunicações automatizadas ou humanas.

### 2. Scope
- **What is included**:
  - Associação de múltiplos contatos para uma única Pessoa (Física ou Jurídica).
  - Título/Descrição daquele contato.
  - Campos específicos para Telefone (Fixo) e WhatsApp.
- **What is excluded**:
  - Disparo real de mensagens via WhatsApp ou telefonia.
  - Representação de endereços físicos ou virtuais (e-mails, redes sociais), caso não estipulados no requisito atual.

### 3. Functional Requirements
- O sistema deve permitir atrelar múltiplos contatos a uma mesma Pessoa.
- O sistema deve exigir um título/cabeçalho identificador para o contato (ex: "Casa", "Financeiro").
- O sistema deve permitir a inclusão de um número de WhatsApp como obrigatório.
- O sistema deve permitir a inclusão de um número de Telefone fixo como opcional.
- O sistema deve permitir leitura, criação, deleção e atualização dos dados de contatos.

### 4. Required Fields
**Entidade Contato**
- Pessoa (Link obrigatório para a entidade dona)
- Título (Exemplo: "Setor Comercial")
- WhatsApp (Obrigatório)
- Telefone Fixo (Opcional)

### 5. Validation Rules (Business-Level)
- Os telefones (Fixo e WhatsApp) devem ser consistentes, contendo apenas números quando persistidos.
- Formatos devem contemplar o DDD e a numeração base brasileira (pelo menos na premissa).
- Um contato obrigatoriamente precisa estar associado a uma Pessoa válida.

### 6. Acceptance Criteria
- Como um operador, ao cadastrar um Contato para uma Empresa (PJ) com o WhatsApp preenchido e o Título, o sistema deve registrar a entrada com sucesso.
- Como um operador, ao cadastrar um Contato, informar o Telefone Fixo em branco deve ser permitido e a operação deve ser bem-sucedida.
- Como um operador, listar os dados de uma Pessoa deve revelar a sua lista de contatos atrelados.

### 7. Non-Functional Requirements
- A busca por contatos deve ser rápida e atrelada via Chave Estrangeira (ForeignKey) ao invés de duplicidade de tabelas no banco de dados.
