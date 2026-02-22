import re
from django.db import transaction
from django.core.exceptions import ValidationError
from pessoa.models import Pessoa, PessoaJuridica

class CreatePessoaJuridicaUseCase:
    """
    Use Case para criação de uma Pessoa Jurídica.
    Garante que a criação da Pessoa (âncora) e da PessoaJuridica ocorra
    de forma atômica no banco de dados.
    """
    
    @transaction.atomic
    def execute(self, razao_social: str, cnpj: str, nome_fantasia: str = None) -> PessoaJuridica:
        # Strip any formatting characters from the CNPJ
        clean_cnpj = re.sub(r'\D', '', cnpj)
        
        # 1. Cria a entidade âncora (Pessoa)
        pessoa = Pessoa.objects.create()
        
        # 2. Cria a entidade específica (Pessoa Jurídica) associada à âncora
        pessoa_juridica = PessoaJuridica(
            pessoa=pessoa,
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            cnpj=clean_cnpj
        )
        
        # O método full_clean executará todas as validações de modelo, incluindo o validate_cnpj customizado
        try:
            pessoa_juridica.full_clean()
        except ValidationError as e:
            # Re-raise the error so the atomic transaction rolls back the base `Pessoa`
            raise e
            
        pessoa_juridica.save()
        return pessoa_juridica
