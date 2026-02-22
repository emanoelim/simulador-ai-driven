from django.db import transaction
from django.core.exceptions import ValidationError
from pessoa.models import Pessoa, Contato
from pessoa.helpers.validators_contato import validate_telefone

class CreateContatoUseCase:
    """
    Use Case para criação de um novo Contato atrelado a uma Pessoa.
    Garante que os telefones sejam sanitizados antes de salvar na base.
    """
    @transaction.atomic
    def execute(self, pessoa_id: str, titulo: str, whatsapp: str, telefone_fixo: str = None) -> Contato:
        try:
            pessoa = Pessoa.objects.get(id=pessoa_id)
        except Pessoa.DoesNotExist:
            raise ValidationError({'pessoa_id': ['Pessoa não encontrada.']})

        clean_whatsapp = validate_telefone(whatsapp)
        clean_telefone = validate_telefone(telefone_fixo) if telefone_fixo else None

        contato = Contato(
            pessoa=pessoa,
            titulo=titulo,
            whatsapp=clean_whatsapp,
            telefone_fixo=clean_telefone
        )

        try:
            contato.full_clean()
        except ValidationError as e:
            raise e
            
        contato.save()
        return contato
