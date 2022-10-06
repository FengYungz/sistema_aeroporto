from django.test import TestCase
# Create your tests here.
from models import Voo
class VooModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Voo.objects.create(codigo='', companhia = '', previsao_chegada = '', previsao_partida = '', data_chegada = '', data_saida = '', status = '', rota = '')
    def test_criacao_id(self):
         Voo_1 = Voo.objects.get(codigo='Os Irmãos Karamazov')
         self.assertEqual(Voo_1.id, 1)

