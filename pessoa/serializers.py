from rest_framework import serializers
from .models import PessoaFisica

class PessoaFisicaSerializer(serializers.ModelSerializer):
    """
    Serializer responsável apenas por validação primária de input
    e formatação de dados na saída (JSON ↔ Objeto).
    NÃO deve conter regras de negócio complexas.
    """
    id = serializers.UUIDField(source='pessoa.id', read_only=True)
    cpf = serializers.CharField(max_length=14)

    class Meta:
        model = PessoaFisica
        fields = ['id', 'nome_completo', 'cpf', 'data_nascimento']

    def validate_cpf(self, value):
        import re
        return re.sub(r'\D', '', value)
