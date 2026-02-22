from django.db import models

class PessoaFisicaManager(models.Manager):
    """
    Manager methods specific to the PessoaFisica model.
    Encapsulates abstract queries out of the API.
    """
    def get_by_cpf(self, cpf):
        """Retorna uma pessoa física específica buscando pelo CPF completo."""
        return self.filter(cpf=cpf).first()

    def get_active_pessoas(self):
        """Exemplo de abstração de query caso tenhamos flags de deleção lógica no futuro."""
        return self.all()

class PessoaJuridicaManager(models.Manager):
    """
    Manager methods specific to the PessoaJuridica model.
    Encapsulates abstract queries out of the API layer.
    """
    def get_by_cnpj(self, cnpj):
        """Retorna uma pessoa jurídica específica buscando pelo CNPJ completo."""
        return self.filter(cnpj=cnpj).first()

    def get_active_pessoas(self):
        """Exemplo de abstração de query caso tenhamos flags de deleção lógica no futuro."""
        return self.all()
