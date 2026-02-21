import re
from datetime import date
from django.core.exceptions import ValidationError

def validate_cpf(cpf: str) -> None:
    """Validador puramente de domínio para a regra de negócio de formato de CPF."""
    cpf_digits = re.sub(r'\D', '', cpf)
    
    if len(cpf_digits) != 11:
        raise ValidationError('CPF deve conter exatamente 11 dígitos numéricos.')
        
    if len(set(cpf_digits)) == 1:
        raise ValidationError('CPF não pode ser uma sequência de números iguais.')
        
    numbers = [int(digit) for digit in cpf_digits]

    def calculate_digit(cpf_partial, weight_start):
        total = sum(digit * weight for digit, weight in zip(cpf_partial, range(weight_start, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    # Calculates the first verification digit
    first_digit = calculate_digit(numbers[:9], 10)
    if first_digit != numbers[9]:
        raise ValidationError('CPF inválido (primeiro dígito verificador incorreto).')

    # Calculates the second verification digit
    second_digit = calculate_digit(numbers[:10], 11)
    if second_digit != numbers[10]:
        raise ValidationError('CPF inválido (segundo dígito verificador incorreto).')

def validate_data_nascimento(data_nascimento: date) -> None:
    """Impede o registro de datas no futuro."""
    if data_nascimento > date.today():
        raise ValidationError('A data de nascimento não pode estar no futuro.')
