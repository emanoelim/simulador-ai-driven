from django.db import models

class PessoaFisicaManager(models.Manager):
    def get_by_cpf(self, cpf):
        """Retorna uma pessoa física específica buscando pelo CPF completo."""
        return self.filter(cpf=cpf).first()

    def get_active_pessoas(self):
        """Exemplo de abstração de query caso tenhamos flags de deleção lógica no futuro."""
        return self.all()
