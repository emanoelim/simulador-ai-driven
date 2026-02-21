from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date
from pessoa.use_cases import CreatePessoaFisicaUseCase
from pessoa.models import Pessoa, PessoaFisica

class CreatePessoaFisicaUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = CreatePessoaFisicaUseCase()
        self.valid_payload = {
            'nome_completo': 'Teste Silva',
            'cpf': '529.982.247-25', # Sent with format mask
            'data_nascimento': date(1990, 1, 1)
        }

    def test_create_pessoa_fisica_success(self):
        pessoa_fisica = self.use_case.execute(**self.valid_payload)
        
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(PessoaFisica.objects.count(), 1)
        self.assertEqual(pessoa_fisica.nome_completo, 'Teste Silva')
        self.assertIsNotNone(pessoa_fisica.pessoa.id)

    def test_create_pessoa_fisica_failure_rolls_back_pessoa(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['cpf'] = '123' # Invalid length
        
        with self.assertRaises(ValidationError):
            self.use_case.execute(**invalid_payload)
            
        # Ensure that if PessoaFisica fails to create/validate, the base Pessoa is not saved (Transaction Atomic check)
        self.assertEqual(Pessoa.objects.count(), 0)
        self.assertEqual(PessoaFisica.objects.count(), 0)
