from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import transaction
from pessoa.models import Pessoa, PessoaJuridica
from pessoa.use_cases import CreatePessoaJuridicaUseCase

class CreatePessoaJuridicaUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = CreatePessoaJuridicaUseCase()

    def test_create_pessoa_juridica_success(self):
        razao_social = "Empresa Teste Ltda"
        nome_fantasia = "Teste"
        cnpj = "11.222.333/0001-81" # with mask
        
        pessoa_juridica = self.use_case.execute(
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            cnpj=cnpj
        )

        self.assertIsInstance(pessoa_juridica, PessoaJuridica)
        self.assertEqual(pessoa_juridica.razao_social, razao_social)
        self.assertEqual(pessoa_juridica.nome_fantasia, nome_fantasia)
        self.assertEqual(pessoa_juridica.cnpj, '11222333000181') # Clean
        
        # Ensures it's correctly linked and saved
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(PessoaJuridica.objects.count(), 1)
        self.assertEqual(pessoa_juridica.pessoa_id, Pessoa.objects.first().id)

    def test_create_pessoa_juridica_validation_rollback(self):
        razao_social = "Empresa Teste Ltda"
        cnpj = "11.222.333/0001-82" # Invalid CNPJ
        
        with self.assertRaises(ValidationError):
            self.use_case.execute(razao_social=razao_social, cnpj=cnpj)

        # Ensures atomic rollback over the Pessoa anchor
        self.assertEqual(Pessoa.objects.count(), 0)
        self.assertEqual(PessoaJuridica.objects.count(), 0)
