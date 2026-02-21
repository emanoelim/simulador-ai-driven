from django.db import transaction
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
        
        # 3. Executa as validações do modelo de dados
        pessoa_fisica.full_clean()
        
        # 4. Persiste no banco de dados
        pessoa_fisica.save()
        
        return pessoa_fisica
