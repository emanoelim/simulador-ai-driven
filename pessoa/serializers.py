from rest_framework import serializers

from .models import PessoaFisica, PessoaJuridica, Contato
from .helpers.validators_pf import validate_cpf
from .helpers.validators_pj import validate_cnpj

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = ['id', 'pessoa', 'titulo', 'telefone_fixo', 'whatsapp', 'created_at']


class PessoaFisicaSerializer(serializers.ModelSerializer):
    """
    Serializer responsável apenas por validação primária de input
    e formatação de dados na saída (JSON ↔ Objeto).
    NÃO deve conter regras de negócio complexas.
    """
    id = serializers.UUIDField(source='pessoa.id', read_only=True)
    cpf = serializers.CharField(max_length=14)
    contatos = ContatoSerializer(source='pessoa.contatos', many=True, read_only=True)

    class Meta:
        model = PessoaFisica
        fields = ['id', 'nome_completo', 'cpf', 'data_nascimento', 'contatos']

    def validate_cpf(self, value):
        """
        Garante que o CPF seja válido e limpo (sem máscara) antes de
        qualquer lógica atômica.
        """
        import re
        validate_cpf(value)
        return re.sub(r'\D', '', value)

class PessoaJuridicaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo PessoaJuridica.
    Responsável por formatar os dados de entrada/saída.
    NÃO deve conter regras de negócio complexas de criação.
    """
    id = serializers.UUIDField(source='pessoa.id', read_only=True)
    cnpj = serializers.CharField(max_length=18)
    contatos = ContatoSerializer(source='pessoa.contatos', many=True, read_only=True)

    class Meta:
        model = PessoaJuridica
        fields = ['id', 'razao_social', 'nome_fantasia', 'cnpj', 'contatos']

    def validate_cnpj(self, value):
        """
        Garante que o CNPJ seja validado matematicamente e devolva
        apenas os números, isolando o UseCase do formato da API.
        """
        import re
        validate_cnpj(value)
        return re.sub(r'\D', '', value)
