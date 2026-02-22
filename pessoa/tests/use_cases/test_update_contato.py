from django.test import TestCase
from django.core.exceptions import ValidationError
from model_bakery import baker
from pessoa.models import Pessoa, Contato
from pessoa.use_cases import UpdateContatoUseCase

class UpdateContatoUseCaseTestCase(TestCase):
    def setUp(self):
        self.use_case = UpdateContatoUseCase()
        self.pessoa = baker.make(Pessoa)
        self.contato = baker.make(Contato, pessoa=self.pessoa, titulo="Antigo", whatsapp="11900000000")

    def test_update_contato_success(self):
        novo_titulo = "Novo Titulo"
        novo_whatsapp = "(21) 98888-8888"
        novo_fixo = "(21) 3333-3333"

        contato_atualizado = self.use_case.execute(
            contato=self.contato,
            titulo=novo_titulo,
            whatsapp=novo_whatsapp,
            telefone_fixo=novo_fixo
        )

        self.assertEqual(contato_atualizado.titulo, novo_titulo)
        self.assertEqual(contato_atualizado.whatsapp, "21988888888")
        self.assertEqual(contato_atualizado.telefone_fixo, "2133333333")
        
        # Ensure it was saved to DB and didn't create a new one
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.titulo, novo_titulo)
        self.assertEqual(Contato.objects.count(), 1)

    def test_update_contato_invalid_phone_rollback(self):
        # Attempt to update with invalid whatsapp
        with self.assertRaises(ValidationError):
            self.use_case.execute(
                contato=self.contato,
                titulo="Novo",
                whatsapp="abc" # Invalid
            )

        # Ensure database state didn't change (rollback)
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.titulo, "Antigo") # Kept old value
        self.assertEqual(self.contato.whatsapp, "11900000000")
