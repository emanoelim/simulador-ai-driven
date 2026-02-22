import uuid
from django.db import models

from .managers import PessoaFisicaManager, PessoaJuridicaManager
from .helpers.validators_pf import validate_cpf
from .helpers.validators_pj import validate_cnpj

class Pessoa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return str(self.id)

class PessoaFisica(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='fisica')
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    data_nascimento = models.DateField()

    objects = PessoaFisicaManager()

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"

class PessoaJuridica(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, primary_key=True)
    razao_social = models.CharField(max_length=255, db_index=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    cnpj = models.CharField(max_length=14, unique=True, validators=[validate_cnpj])

    objects = PessoaJuridicaManager()

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

class Contato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='contatos')
    titulo = models.CharField(max_length=100)
    telefone_fixo = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return f"{self.titulo} - {self.pessoa}"