from django.db import transaction
from django.core.exceptions import ValidationError
from pessoa.models import Contato
from pessoa.helpers.validators_contato import validate_telefone

class UpdateContatoUseCase:
    """
    Use Case para atualização de um Contato existente.
    Garante re-higienização caso novos números sejam fornecidos.
    """
    @transaction.atomic
    def execute(self, contato: Contato, titulo: str, whatsapp: str, telefone_fixo: str = None) -> Contato:
        clean_whatsapp = validate_telefone(whatsapp)
        clean_telefone = validate_telefone(telefone_fixo) if telefone_fixo else None

        contato.titulo = titulo
        contato.whatsapp = clean_whatsapp
        contato.telefone_fixo = clean_telefone
        
        try:
            contato.full_clean()
        except ValidationError as e:
            raise e
            
        contato.save()
        return contato
