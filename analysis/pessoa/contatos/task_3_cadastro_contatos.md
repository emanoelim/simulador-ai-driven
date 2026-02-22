# Technical Analysis: Cadastro de Contatos (Pessoa)

## 1. Visão Geral
A funcionalidade de **Contatos** permite atrelar meios de comunicação (focados inicialmente em WhatsApp e Telefone Fixo) a qualquer entidade do tipo `Pessoa` (Física ou Jurídica). O objetivo arquitetural é utilizar a estrutura de chave estrangeira com a entidade base `Pessoa` para suportar tanto clientes físicos quanto empresas de forma homogênea.

## 2. Abordagem Arquitetural (Clean Architecture)

### 2.1 Domain Layer (Models)
A entidade `Contato` ficará em `pessoa/models.py`.

```python
class Contato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Vinculado à raiz Pessoa, permitindo contatos tanto para PJ quanto PF
    pessoa = models.ForeignKey('Pessoa', on_delete=models.CASCADE, related_name='contatos')
    titulo = models.CharField(max_length=100) # Ex: Pessoal, Cobrança, Sócio
    telefone_fixo = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
```

### 2.2 Repositories (Managers)
Será utilizado o ORM nativo por meio de *reverse relation* (`pessoa.contatos.all()`). Não há necessidade complexa de Managers abstratos para `Contato` neste primeiro momento.

### 2.3 Services / Helpers (Validators)
Criaremos validações numéricas para o telefone e whatsapp, garantindo sanitização na gravação.
- Arquivo: `pessoa/helpers/validators_contato.py`
- Função estrita: `validate_telefone(value)`: Valida e remove caracteres de máscara `() -`.

### 2.4 Use Cases
Garantem consistência atômica da gravação de um Contato:
- `CreateContatoUseCase`: Executa a rotina de validação e criação atômica. Recebe uma UUID de Pessoa ou a própria instância.
- `UpdateContatoUseCase`: Possibilita alteração dos dados, sanitizando novamente telefones.

### 2.5 API e ViewSets
1. **ModelViewSet**: `ContatoViewSet` responsável por C.R.U.D de `/api/contatos/` (ou `/api/pessoas/<id>/contatos/`).
2. **Serializers**:
   - `ContatoSerializer`: Expõe título, telefone fixo e WhatsApp.
   - Os serializers de `PessoaFisica` e `PessoaJuridica` serão atualizados para possuírem um método `Nested Serializer` (`contatos = ContatoSerializer(many=True, read_only=True)`) visando entregar ao Front-end a ficha completa do indivíduo ou empresa.

## 3. Estratégia de Testes (Baseado no test_standard.md)
- **Helpers**: Testes unitários puros isolados contra máscaras para telefones (`django.test.TestCase`).
- **Use Cases**: Testar atomicidade e vinculação (deve falhar sem pessoa). Utilizar `django.test.TestCase`.
- **API**: Testes de requisições POST, UPDATE com dados válidos e telefones mal formatados testando *Bad Requests*. Utilizar restritamente `rest_framework.test.APITestCase`.
- **Massa de Dados**: Utilizar obrigatoriamente `model_bakery` para instanciar as Pessoas de teste em vez de `objects.create()`.
