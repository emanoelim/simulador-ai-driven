import re
from django.core.exceptions import ValidationError

def validate_telefone(value: str) -> str:
    """
    Remove todos os caracteres não numéricos do telefone.
    Garante que tenha pelo menos 10 dígitos (DDD + 8 dígitos) e no máximo 11 (DDD + 9 dígitos).
    """
    if not value:
        raise ValidationError('O telefone não pode ser vazio.')
        
    clean_phone = re.sub(r'\D', '', value)

    if not clean_phone:
        raise ValidationError('O telefone não pode ficar vazio após a remoção de formatação.')

    if len(clean_phone) < 10 or len(clean_phone) > 11:
        raise ValidationError('O telefone deve ter 10 ou 11 dígitos numéricos (com DDD).')

    return clean_phone
