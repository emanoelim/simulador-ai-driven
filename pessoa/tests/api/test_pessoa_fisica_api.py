from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from pessoa.models import Pessoa, PessoaFisica
import datetime

class PessoaFisicaAPITestCase(APITestCase):
    def setUp(self):
        # We manually register the router in tests if url reversing needs it, but we can also use fixed paths.
        self.list_url = '/api/pessoas/fisicas/'
        
    def test_create_pessoa_fisica(self):
        payload = {
            'nome_completo': 'John Doe API',
            'cpf': '012.345.678-90', # Sent with format mask
            'data_nascimento': '1985-05-15'
        }
        
        response = self.client.post(self.list_url, data=payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(PessoaFisica.objects.count(), 1)

    def test_create_duplicate_cpf_returns_400(self):
        # Using model_bakery to create an existing record
        base_pessoa = baker.make('pessoa.Pessoa')
        baker.make('pessoa.PessoaFisica', pessoa=base_pessoa, cpf='52998224725')
        
        payload = {
            'nome_completo': 'Jane Doe',
            'cpf': '52998224725', # Duplicate
            'data_nascimento': '1990-01-01'
        }
        
        response = self.client.post(self.list_url, data=payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PessoaFisica.objects.count(), 1) # Only the baked one remains
