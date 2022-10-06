from django.test import TestCase
import datetime
# Create your tests here.
from book.models import Voo

class VooModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Voo.objects.create(codigo='GOL45568', companhia = 'GOL', previsao_chegada = '2006-10-25 14:30:59', previsao_partida = '2006-10-24 14:30:59', status = 'finalizado', rota = 'RioSaoPaulo')
    
    def test_criacao_id(self):
         Voo_1 = Voo.objects.get(codigo='GOL45568')
         self.assertEqual(Voo_1.id, 1)

    def test_criacao_falsa_id(self):
         Voo_1 = Voo.objects.get(codigo='GOL00787')
         self.assertEqual(Voo_1.id, 1)

   

