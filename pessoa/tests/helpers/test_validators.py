from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from pessoa.helpers.validators import validate_cpf, validate_data_nascimento

class ValidatorsTestCase(TestCase):
    def test_validate_cpf_with_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_cpf('1234567890')
        self.assertIn('11 dígitos', str(context.exception))

    def test_validate_cpf_with_sequential_numbers(self):
        with self.assertRaises(ValidationError) as context:
            validate_cpf('11111111111')
        self.assertIn('sequência de números iguais', str(context.exception))

    def test_validate_cpf_invalid_first_digit(self):
        # CPF base valid, but last two digits manually changed to fail first digit
        with self.assertRaises(ValidationError) as context:
            validate_cpf('52998224735') # Valid is 52998224725
        self.assertIn('primeiro dígito verificador incorreto', str(context.exception))

    def test_validate_cpf_invalid_second_digit(self):
        # Valid up to first digit, but second digit changed to fail (Valid is 52998224725)
        with self.assertRaises(ValidationError) as context:
            validate_cpf('52998224726')
        self.assertIn('segundo dígito verificador incorreto', str(context.exception))

    def test_validate_cpf_success(self):
        # Real mathematical valid CPF
        validate_cpf('52998224725')
        validate_cpf('01234567890')
        self.assertTrue(True)

    def test_validate_data_nascimento_future_date(self):
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError) as context:
            validate_data_nascimento(future_date)
        self.assertIn('futuro', str(context.exception))

    def test_validate_data_nascimento_valid_date(self):
        past_date = date.today() - timedelta(days=1)
        validate_data_nascimento(past_date)
        self.assertTrue(True)
