from django.test import TestCase
# Create your tests here.
from models import Voo
class VooModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Voo.objects.create(codigo='Os Irmãos Karamazov')
    def test_criacao_id(self):
         Voo_1 = Voo.objects.get(titulo='Os Irmãos Karamazov')
         self.assertEqual(Voo_1.id, 1)