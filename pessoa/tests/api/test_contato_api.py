from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from pessoa.models import Pessoa, Contato

class ContatoAPITestCase(APITestCase):
    def setUp(self):
        self.pessoa = baker.make(Pessoa)
        self.contato_url = reverse('contato-list')
        
    def test_create_contato_success(self):
        payload = {
            'pessoa': str(self.pessoa.id),
            'titulo': 'Meu Contato',
            'whatsapp': '(11) 98765-4321',
            'telefone_fixo': '(11) 4002-8922'
        }
        response = self.client.post(self.contato_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['whatsapp'], '11987654321')
        self.assertEqual(response.data['telefone_fixo'], '1140028922')
        self.assertEqual(Contato.objects.count(), 1)

    def test_create_contato_invalid_phone(self):
        payload = {
            'pessoa': str(self.pessoa.id),
            'titulo': 'Invalido',
            'whatsapp': '123'
        }
        response = self.client.post(self.contato_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('10 ou 11 dígitos', str(response.data))

    def test_update_contato_success(self):
        contato = baker.make(Contato, pessoa=self.pessoa, titulo='Antigo', whatsapp='11900000000')
        url = reverse('contato-detail', args=[str(contato.id)])
        
        payload = {
            'pessoa': str(self.pessoa.id),
            'titulo': 'Novo',
            'whatsapp': '(21) 98888-8888'
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contato.refresh_from_db()
        self.assertEqual(contato.titulo, 'Novo')
        self.assertEqual(contato.whatsapp, '21988888888')

    def test_delete_contato_success(self):
        contato = baker.make(Contato, pessoa=self.pessoa)
        url = reverse('contato-detail', args=[str(contato.id)])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contato.objects.count(), 0)
