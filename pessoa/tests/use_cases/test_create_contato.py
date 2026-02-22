from django.test import TestCase
from django.core.exceptions import ValidationError
from model_bakery import baker
from pessoa.models import Pessoa, Contato
from pessoa.use_cases import CreateContatoUseCase

class CreateContatoUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = CreateContatoUseCase()
        # model_bakery instance as per test_standard.md
        self.pessoa = baker.make(Pessoa)

    def test_create_contato_success(self):
        titulo = "Telefone Pessoal"
        whatsapp = "(11) 98765-4321"
        telefone_fixo = "(11) 4002-8922"

        contato = self.use_case.execute(
            pessoa_id=self.pessoa.id,
            titulo=titulo,
            whatsapp=whatsapp,
            telefone_fixo=telefone_fixo
        )

        self.assertIsInstance(contato, Contato)
        self.assertEqual(contato.titulo, titulo)
        self.assertEqual(contato.whatsapp, "11987654321") # Cleaned
        self.assertEqual(contato.telefone_fixo, "1140028922") # Cleaned
        self.assertEqual(contato.pessoa.id, self.pessoa.id)
        self.assertEqual(Contato.objects.count(), 1)

    def test_create_contato_without_telefone_fixo(self):
        contato = self.use_case.execute(
            pessoa_id=self.pessoa.id,
            titulo="Apenas Celular",
            whatsapp="(21) 99999-9999"
        )
        self.assertEqual(contato.telefone_fixo, None)
        self.assertEqual(contato.whatsapp, "21999999999")

    def test_create_contato_unlinked_pessoa_rollback(self):
        import uuid
        fake_id = uuid.uuid4()
        
        with self.assertRaises(ValidationError) as context:
            self.use_case.execute(
                pessoa_id=fake_id,
                titulo="Ghost",
                whatsapp="11987654321"
            )
            
        self.assertIn('Pessoa não encontrada.', str(context.exception))
        self.assertEqual(Contato.objects.count(), 0)

    def test_create_contato_invalid_phone_rollback(self):
        with self.assertRaises(ValidationError) as context:
            self.use_case.execute(
                pessoa_id=self.pessoa.id,
                titulo="Inválido",
                whatsapp="123" # too short
            )
            
        self.assertIn('10 ou 11 dígitos', str(context.exception))
        self.assertEqual(Contato.objects.count(), 0)
