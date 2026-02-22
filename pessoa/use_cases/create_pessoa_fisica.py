from django.db import transaction
from django.core.exceptions import ValidationError
from pessoa.models import Pessoa, PessoaFisica
from datetime import date

class CreatePessoaFisicaUseCase:
    """
    Orquestra a criação atômica de uma entidade base Pessoa e a sua
    respectiva PessoaFisica com as validações de domínio atreladas.
    """
    
    @transaction.atomic
    def execute(self, nome_completo: str, cpf: str, data_nascimento: date) -> PessoaFisica:
        # Strip any formatting characters from the CPF
        import re
        clean_cpf = re.sub(r'\D', '', cpf)
        
        # 1. Cria a entidade âncora (Pessoa)
        pessoa = Pessoa.objects.create()
        
        # 2. Cria a entidade específica (Pessoa Física) associada à âncora
        pessoa_fisica = PessoaFisica(
            pessoa=pessoa,
            nome_completo=nome_completo,
            cpf=clean_cpf,
            data_nascimento=data_nascimento
        )
        
        # O método full_clean executará todas as validações de modelo, incluindo o validate_cpf customizado
        try:
            pessoa_fisica.full_clean()
        except ValidationError as e:
            # Re-raise the error so the atomic transaction rolls back the base `Pessoa`
            raise e
            
        # 4. Persiste no banco de dados
        pessoa_fisica.save()
        
        return pessoa_fisica
