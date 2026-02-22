import re
from django.db import transaction
from django.core.exceptions import ValidationError
from pessoa.models import PessoaJuridica

class UpdatePessoaJuridicaUseCase:
    """
    Use Case para atualização de uma Pessoa Jurídica existente.
    Mantém as regras de negócio puras isoladas da camada de API.
    A atualização do CNPJ pode ser bloqueada aqui no futuro se for uma regra de negócio.
    Por enquanto, aceitamos atualização total.
    """
    
    @transaction.atomic
    def execute(self, pessoa_juridica: PessoaJuridica, razao_social: str, cnpj: str, nome_fantasia: str = None) -> PessoaJuridica:
        clean_cnpj = re.sub(r'\D', '', cnpj)
        
        pessoa_juridica.razao_social = razao_social
        pessoa_juridica.nome_fantasia = nome_fantasia
        pessoa_juridica.cnpj = clean_cnpj
        
        try:
            pessoa_juridica.full_clean()
        except ValidationError as e:
            raise e
            
        pessoa_juridica.save()
        return pessoa_juridica
