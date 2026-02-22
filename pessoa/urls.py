from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PessoaFisicaViewSet, PessoaJuridicaViewSet, ContatoViewSet

router = DefaultRouter()
router.register(r'fisicas', PessoaFisicaViewSet, basename='pessoafisica')
router.register(r'juridicas', PessoaJuridicaViewSet, basename='pessoajuridica')
router.register(r'contatos', ContatoViewSet, basename='contato')

urlpatterns = [
    path('', include(router.urls)),
]
