from django.test import TestCase
from django.core.exceptions import ValidationError
from model_bakery import baker
from pessoa.models import PessoaJuridica
from pessoa.use_cases import UpdatePessoaJuridicaUseCase

class UpdatePessoaJuridicaUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = UpdatePessoaJuridicaUseCase()
        self.pessoa_juridica = baker.make('pessoa.PessoaJuridica', cnpj='11222333000181')

    def test_update_pessoa_juridica_success(self):
        new_razao_social = "Nova Empresa S.A."
        new_cnpj = "56.996.342/0001-68" # With mask, valid
        
        updated_pessoa = self.use_case.execute(
            pessoa_juridica=self.pessoa_juridica,
            razao_social=new_razao_social,
            nome_fantasia="Novo Nome",
            cnpj=new_cnpj
        )

        self.assertEqual(updated_pessoa.razao_social, new_razao_social)
        self.assertEqual(updated_pessoa.nome_fantasia, "Novo Nome")
        self.assertEqual(updated_pessoa.cnpj, '56996342000168') # Cleaned
        
        # Refetch from DB to ensure save
        pessoa_db = PessoaJuridica.objects.get(pessoa_id=self.pessoa_juridica.pessoa_id)
        self.assertEqual(pessoa_db.razao_social, new_razao_social)
        self.assertEqual(pessoa_db.cnpj, '56996342000168')

    def test_update_pessoa_juridica_validation_error(self):
        invalid_cnpj = "56.996.342/0001-73" # Invalid CNPJ (wrong digit)
        
        with self.assertRaises(ValidationError):
            self.use_case.execute(
                pessoa_juridica=self.pessoa_juridica,
                razao_social=self.pessoa_juridica.razao_social,
                cnpj=invalid_cnpj
            )

        # Ensure no change in DB
        pessoa_db = PessoaJuridica.objects.get(pessoa_id=self.pessoa_juridica.pessoa_id)
        self.assertEqual(pessoa_db.cnpj, '11222333000181') # Original CNPJ
