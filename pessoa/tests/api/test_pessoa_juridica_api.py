from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from pessoa.models import Pessoa, PessoaJuridica

class PessoaJuridicaAPITestCase(APITestCase):
    def setUp(self):
        self.list_url = '/api/pessoas/juridicas/'
        
    def test_create_pessoa_juridica(self):
        payload = {
            'razao_social': 'Empresa Demo Ltda',
            'nome_fantasia': 'Demo',
            'cnpj': '11.222.333/0001-81' # With mask
        }
        
        response = self.client.post(self.list_url, data=payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(PessoaJuridica.objects.count(), 1)

    def test_create_duplicate_cnpj_returns_400(self):
        # Create an existing record
        base_pessoa = baker.make('pessoa.Pessoa')
        baker.make('pessoa.PessoaJuridica', pessoa=base_pessoa, cnpj='11222333000181')
        
        payload = {
            'razao_social': 'Outra Empresa',
            'cnpj': '11222333000181' # Duplicate
        }
        
        response = self.client.post(self.list_url, data=payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PessoaJuridica.objects.count(), 1)

    def test_update_pessoa_juridica(self):
        base_pessoa = baker.make('pessoa.Pessoa')
        p_juridica = baker.make('pessoa.PessoaJuridica', pessoa=base_pessoa, cnpj='11222333000181')
        
        detail_url = f'{self.list_url}{base_pessoa.id}/'
        payload = {
            'razao_social': 'Empresa Atualizada',
            'cnpj': '56.996.342/0001-68'
        }
        
        response = self.client.put(detail_url, data=payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        p_juridica.refresh_from_db()
        self.assertEqual(p_juridica.razao_social, 'Empresa Atualizada')
        self.assertEqual(p_juridica.cnpj, '56996342000168')
