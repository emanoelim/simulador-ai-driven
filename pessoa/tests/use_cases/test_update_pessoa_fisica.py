from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from model_bakery import baker
from pessoa.use_cases import UpdatePessoaFisicaUseCase
from pessoa.models import PessoaFisica

class UpdatePessoaFisicaUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = UpdatePessoaFisicaUseCase()
        
        # Setup using model_bakery, bypassing the create use case so we have a clean DB state
        # using a valid CPF for the fixture
        base_pessoa = baker.make('pessoa.Pessoa')
        self.pessoa_fisica = baker.make(
            'pessoa.PessoaFisica', 
            pessoa=base_pessoa, 
            nome_completo='Old Name', 
            cpf='52998224725', 
            data_nascimento=date(1990, 1, 1)
        )

    def test_update_pessoa_fisica_success(self):
        new_date = date(1995, 5, 5)
        
        updated_pf = self.use_case.execute(
            pessoa_fisica=self.pessoa_fisica,
            nome_completo='New Name',
            data_nascimento=new_date
        )
        
        # Verify the returned object
        self.assertEqual(updated_pf.nome_completo, 'New Name')
        self.assertEqual(updated_pf.data_nascimento, new_date)
        
        # Verify from DB explicitly
        pf_db = PessoaFisica.objects.get(pk=self.pessoa_fisica.pk)
        self.assertEqual(pf_db.nome_completo, 'New Name')
        self.assertEqual(pf_db.data_nascimento, new_date)
        
        # CPF should not be modified
        self.assertEqual(pf_db.cpf, '52998224725')

    def test_update_pessoa_fisica_invalid_data_rolls_back(self):
        # Empty string should fail model validation (full_clean)
        with self.assertRaises(ValidationError):
            self.use_case.execute(
                pessoa_fisica=self.pessoa_fisica,
                nome_completo='', # This isn't allowed
                data_nascimento=date(1990, 1, 1)
            )
            
        # Ensure DB was not updated
        pf_db = PessoaFisica.objects.get(pk=self.pessoa_fisica.pk)
        self.assertEqual(pf_db.nome_completo, 'Old Name')
