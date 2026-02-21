from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaFisicaViewSet

router = DefaultRouter()
router.register(r'fisicas', PessoaFisicaViewSet, basename='pessoafisica')

urlpatterns = [
    path('', include(router.urls)),
]
