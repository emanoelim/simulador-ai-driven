import uuid
from django.db import models

from .managers import PessoaFisicaManager
from .helpers.validators import validate_cpf

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
