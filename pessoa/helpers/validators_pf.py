from datetime import date
from django.core.exceptions import ValidationError

def validate_cpf(value: str):
    """
    Realiza a validação matemática do CPF.
    """
    import re
    # Remove qualquer caractere não numérico antes de validar
    cpf = re.sub(r'\D', '', value)

    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter 11 dígitos (após remover a formatação).')

    if len(set(cpf)) == 1:
        raise ValidationError('CPF inválido (sequência de números iguais).')

    # Validação do primeiro dígito verificador
    sum_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder_1 = (sum_1 * 10) % 11
    if remainder_1 == 10:
        remainder_1 = 0
        
    if int(cpf[9]) != remainder_1:
        raise ValidationError('CPF inválido (primeiro dígito verificador incorreto).')

    # Validação do segundo dígito verificador
    sum_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder_2 = (sum_2 * 10) % 11
    if remainder_2 == 10:
        remainder_2 = 0

    if int(cpf[10]) != remainder_2:
        raise ValidationError('CPF inválido (segundo dígito verificador incorreto).')

def validate_data_nascimento(data_nascimento: date):
    """Impede o registro de datas no futuro."""
    if data_nascimento > date.today():
        raise ValidationError('A data de nascimento não pode estar no futuro.')
