from django.test import TestCase
import datetime
# Create your tests here.
from book.models import Voo, Estado_Dinamico
 
class VooModelTest(TestCase):
   
    @classmethod
    def setUpTestData(cls):
         Voo.objects.create(codigo='TAM45568', companhia = 'TAM', previsao_chegada = '2006-10-25 14:30:59', previsao_partida = '2006-10-24 14:30:59', rota = 'RioSaoPaulo')
         Voo.objects.create(codigo='GOL45568', companhia = 'GOL', previsao_chegada = '2006-10-25 14:30:59', previsao_partida = '2006-10-24 14:30:59', rota = 'RioSaoPaulo')
         
         Estado_Dinamico.objects.create(codigo='TAM45568', data_chegada = '2006-10-25 14:30:59', data_saida = '2006-10-24 14:30:59', status = 'FIN')
         Estado_Dinamico.objects.create(codigo='GOL45568', data_chegada = '2006-10-25 14:30:59', data_saida = '2006-10-24 14:30:59', status = 'EMB')
 
       
       
 
    def test_criacao_id(self):
         Voo_1 = Voo.objects.get(codigo='TAM45568')
         Voo_2 = Voo.objects.get(codigo='GOL45568')
         self.assertEqual(Voo_1.id, 1)
         self.assertEqual(Voo_2.id, 2)
 
         estado_1 = Estado_Dinamico.objects.get(codigo='TAM45568')
         estado_2 = Estado_Dinamico.objects.get(codigo='GOL45568')
         self.assertEqual(estado_1.id, 1)
         self.assertEqual(estado_1.status, 'FIN')
         self.assertEqual(estado_2.id, 2)
 
    def test_delete_id(self):
         tamInicial = len(Voo.objects.all())
         Voo.objects.filter(id=2).delete()
         tamInicial2 = len(Estado_Dinamico.objects.all())
         Estado_Dinamico.objects.filter(id=1).delete()
 
         tamFinal = len(Voo.objects.all())
         self.assertEqual(tamFinal, tamInicial - 1)
 
         tamFinal2 = len(Estado_Dinamico.objects.all())
         self.assertEqual(tamFinal2, tamInicial2 - 1)
 
    def test_update(self):
        voo_1 =  Voo.objects.get(codigo='GOL45568')
        voo_1.rota = 'SaoPauloRio'
        voo_1.save()
        voo_1_up =  Voo.objects.get(codigo='GOL45568')
        self.assertEqual(voo_1_up.rota, 'SaoPauloRio')