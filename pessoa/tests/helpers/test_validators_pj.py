from django.test import TestCase
from django.core.exceptions import ValidationError
from pessoa.helpers.validators_pj import validate_cnpj

class ValidatorsPJTestCase(TestCase):
    def test_validate_cnpj_with_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_cnpj('123')
        self.assertIn('14 dígitos', str(context.exception))

    def test_validate_cnpj_with_sequential_numbers(self):
        with self.assertRaises(ValidationError) as context:
            validate_cnpj('11111111111111')
        self.assertIn('todos os dígitos repetidos', str(context.exception))

    def test_validate_cnpj_invalid_first_digit(self):
        # Valid CNPJ is 11222333000181. Changing first digit (12th pos)
        with self.assertRaises(ValidationError) as context:
            validate_cnpj('11222333000191')
        self.assertIn('primeiro dígito verificador incorreto', str(context.exception))

    def test_validate_cnpj_invalid_second_digit(self):
        # Valid CNPJ is 11222333000181. Changing second digit (13th pos)
        with self.assertRaises(ValidationError) as context:
            validate_cnpj('11222333000182')
        self.assertIn('segundo dígito verificador incorreto', str(context.exception))

    def test_validate_cnpj_success(self):
        # Valid CNPJ with and without mask
        validate_cnpj('11.222.333/0001-81')
        validate_cnpj('11222333000181')
        self.assertTrue(True)
