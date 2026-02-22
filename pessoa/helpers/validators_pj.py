from django.core.exceptions import ValidationError

def validate_cnpj(value: str):
    """
    Realiza a validação matemática do CNPJ.
    """
    import re
    # Remove qualquer máscara antes de validar
    cnpj = re.sub(r'\D', '', value)

    if len(cnpj) != 14:
        raise ValidationError('O CNPJ deve ter 14 dígitos (após remover a formatação).')

    if len(set(cnpj)) == 1:
        raise ValidationError('CNPJ inválido (todos os dígitos repetidos).')

    # Validação do primeiro dígito verificador
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = sum(int(cnpj[i]) * weights_1[i] for i in range(12))
    remainder_1 = sum_1 % 11
    digit_1 = 0 if remainder_1 < 2 else 11 - remainder_1

    if int(cnpj[12]) != digit_1:
        raise ValidationError('CNPJ inválido (primeiro dígito verificador incorreto).')

    # Validação do segundo dígito verificador
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_2 = sum(int(cnpj[i]) * weights_2[i] for i in range(13))
    remainder_2 = sum_2 % 11
    digit_2 = 0 if remainder_2 < 2 else 11 - remainder_2

    if int(cnpj[13]) != digit_2:
        raise ValidationError('CNPJ inválido (segundo dígito verificador incorreto).')
