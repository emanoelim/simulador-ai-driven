from django.test import TestCase
from django.core.exceptions import ValidationError
from pessoa.helpers.validators_contato import validate_telefone

class ValidatorsContatoTestCase(TestCase):
    def test_validate_telefone_removes_mask(self):
        clean = validate_telefone('(11) 98765-4321')
        self.assertEqual(clean, '11987654321')

    def test_validate_telefone_invalid_length_short(self):
        with self.assertRaises(ValidationError) as context:
            validate_telefone('123456789') # 9 digits
        self.assertIn('10 ou 11 dígitos', str(context.exception))

    def test_validate_telefone_invalid_length_long(self):
        with self.assertRaises(ValidationError) as context:
            validate_telefone('119876543210') # 12 digits
        self.assertIn('10 ou 11 dígitos', str(context.exception))

    def test_validate_telefone_letters_only(self):
        with self.assertRaises(ValidationError) as context:
            validate_telefone('abcdefghij')
        self.assertIn('não pode ficar vazio', str(context.exception))
        
    def test_validate_telefone_empty_string(self):
        with self.assertRaises(ValidationError) as context:
            validate_telefone('')
        self.assertIn('não pode ser vazio', str(context.exception))
