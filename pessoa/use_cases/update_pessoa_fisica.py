from django.db import transaction
from pessoa.models import PessoaFisica
from datetime import date

class UpdatePessoaFisicaUseCase:
    """
    Orquestra a atualização dos dados de uma PessoaFisica atômica.
    """
    
    @transaction.atomic
    def execute(self, pessoa_fisica: PessoaFisica, nome_completo: str, data_nascimento: date) -> PessoaFisica:
        # Nota: O CPF não é atualizado por regras de negócio padrão
        pessoa_fisica.nome_completo = nome_completo
        pessoa_fisica.data_nascimento = data_nascimento
        
        # Executa validações de modelo internamente antes de salvar
        pessoa_fisica.full_clean()
        
        pessoa_fisica.save()
        return pessoa_fisica
