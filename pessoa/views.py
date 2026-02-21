from rest_framework import viewsets
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from .models import PessoaFisica
from .serializers import PessoaFisicaSerializer
from .use_cases import CreatePessoaFisicaUseCase, UpdatePessoaFisicaUseCase

class PessoaFisicaViewSet(viewsets.ModelViewSet):
    """
    View responsável apenas pela Exposição HTTP.
    Delega as execuções restritas aos Use Cases da arquitetura.
    """
    queryset = PessoaFisica.objects.select_related('pessoa').all()
    serializer_class = PessoaFisicaSerializer

    def perform_create(self, serializer):
        use_case = CreatePessoaFisicaUseCase()
        try:
            # Chama o use case puro e acopla a instância retornada ao serializer 
            # (para que a view possa gerar o JSON de payload de retorno 201)
            instance = use_case.execute(
                nome_completo=serializer.validated_data['nome_completo'],
                cpf=serializer.validated_data['cpf'],
                data_nascimento=serializer.validated_data['data_nascimento']
            )
            serializer.instance = instance
        except DjangoValidationError as e:
            # Converte a exceção de domínio interna do Django para a exceção HTTP do DRF (400)
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

    def perform_update(self, serializer):
        use_case = UpdatePessoaFisicaUseCase()
        try:
            instance = use_case.execute(
                pessoa_fisica=self.get_object(),
                nome_completo=serializer.validated_data.get('nome_completo', self.get_object().nome_completo),
                data_nascimento=serializer.validated_data.get('data_nascimento', self.get_object().data_nascimento)
            )
            serializer.instance = instance
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
