from rest_framework import viewsets
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from .models import PessoaFisica, PessoaJuridica, Contato
from .serializers import PessoaFisicaSerializer, PessoaJuridicaSerializer, ContatoSerializer
from .use_cases import (
    CreatePessoaFisicaUseCase, 
    UpdatePessoaFisicaUseCase,
    CreatePessoaJuridicaUseCase,
    UpdatePessoaJuridicaUseCase,
    CreateContatoUseCase,
    UpdateContatoUseCase
)

class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

    def perform_create(self, serializer):
        use_case = CreateContatoUseCase()
        try:
            contato = use_case.execute(
                pessoa_id=str(serializer.validated_data['pessoa'].id),
                titulo=serializer.validated_data['titulo'],
                whatsapp=serializer.validated_data['whatsapp'],
                telefone_fixo=serializer.validated_data.get('telefone_fixo')
            )
            serializer.instance = contato
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

    def perform_update(self, serializer):
        instance = self.get_object()
        use_case = UpdateContatoUseCase()
        try:
            serializer.instance = use_case.execute(
                contato=instance,
                titulo=serializer.validated_data.get('titulo', instance.titulo),
                whatsapp=serializer.validated_data.get('whatsapp', instance.whatsapp),
                telefone_fixo=serializer.validated_data.get('telefone_fixo', instance.telefone_fixo)
            )
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

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
            instance = self.get_object()
            serializer.instance = use_case.execute(
                pessoa_fisica=instance,
                nome_completo=serializer.validated_data.get('nome_completo', instance.nome_completo),
                data_nascimento=serializer.validated_data.get('data_nascimento', instance.data_nascimento)
            )
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

class PessoaJuridicaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciamento de Pessoas Jurídicas.
    Delega a lógica de negócio (criação e atualização atômica) para Use Cases.
    """
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer

    def perform_create(self, serializer):
        use_case = CreatePessoaJuridicaUseCase()
        try:
            pessoa_juridica = use_case.execute(
                razao_social=serializer.validated_data['razao_social'],
                cnpj=serializer.validated_data['cnpj'],
                nome_fantasia=serializer.validated_data.get('nome_fantasia')
            )
            serializer.instance = pessoa_juridica
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

    def perform_update(self, serializer):
        instance = self.get_object()
        use_case = UpdatePessoaJuridicaUseCase()
        try:
            serializer.instance = use_case.execute(
                pessoa_juridica=instance,
                razao_social=serializer.validated_data.get('razao_social', instance.razao_social),
                cnpj=serializer.validated_data.get('cnpj', instance.cnpj),
                nome_fantasia=serializer.validated_data.get('nome_fantasia', instance.nome_fantasia)
            )
        except DjangoValidationError as e:
            raise DrfValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
