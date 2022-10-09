from django.test import TestCase
import datetime
# Create your tests here.
from book.models import Voo, Estado_Dinamico

class VooModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Deixa a indentação bonitinha assim,
		# senão é ruim de enxergar(e editar)
		Voo.objects.create(
			codigo='GOL1',
			companhia = 'GOL',
			previsao_chegada = '2006-10-25 14:30:59',
			previsao_partida = '2006-10-24 14:30:59',
			rota = 'RioSaoPaulo')

		Voo.objects.create(
			codigo='TRAVE1',
			companhia = 'TRAVE',
			previsao_chegada = '2006-10-25 14:30:59',
			previsao_partida = '2006-10-24 14:30:59',
			rota = 'RioSaoPaulo')

		Voo.objects.create(
			codigo='ESCANTEIO1',
			companhia = 'ESCANTEIO',
			previsao_chegada = '2006-11-25 15:30:59',
			previsao_partida = '2006-11-24 15:30:59',
			rota = 'RioSaoPaulo')

		Voo.objects.create(
			codigo='GOL2',
			companhia = 'GOL',
			previsao_chegada = '2007-10-25 14:30:59',
			previsao_partida = '2007-10-24 14:30:59',
			rota = 'SaoPauloRio')

		Estado_Dinamico.objects.create(
			codigo='GOL1',
			companhia = 'GOL',
			data_chegada = '2006-10-25 14:30:59',
			data_partida = '2006-10-24 14:30:59',
			status = 'FIN')

		Estado_Dinamico.objects.create(
			codigo='GOL2',
			companhia = 'GOL',
			data_chegada = '2006-10-25 14:30:59',
			data_partida = '2006-10-24 14:30:59',
			status = 'EMB')

		Estado_Dinamico.objects.create(
			codigo='TRAVE1',
			companhia = 'TRAVE',
			data_chegada = '2006-10-25 14:30:59',
			data_partida = '2006-10-24 14:30:59',
			status = 'FIN')



	def test_criacao(self):
		voo_1 = Voo.objects.get(codigo='GOL1')
		voo_2 = Voo.objects.get(codigo='TRAVE1')
		self.assertEqual(voo_1.id, 1)
		self.assertFalse(voo_1.id, 2)
		self.assertEqual(voo_2.id, 2)

		estado_1 = Estado_Dinamico.objects.get(codigo='GOL1')
		estado_2 = Estado_Dinamico.objects.get(codigo='GOL2')
		self.assertEqual(estado_1.id, 1)
		self.assertEqual(estado_1.data_chegada, '2006-10-25 14:30:59')
		self.assertEqual(estado_2.id, 2)

	# Nao lembro como é o retorno desses comentados abaixo
	# e não estou rodando na minha maquina, só editando o texto

	# def test_filter(self):
	# 	voos_1 = Voo.objects.filter(companhia = 'GOL')
	# 	self.assertEqual(voos_1, ?)

	# def test_order_by(self):
	# 	voos_1 = Voo.objects.order_by('companhia')
	# 	self.assertEqual(voos_1.?, ?)

	def test_update(self):
		voo_1 =  Voo.objects.get(codigo='GOL1')
		voo_1.rota = 'SaoPauloRio'
		voo_1.save()
		voo_1_up =  Voo.objects.get(codigo='GOL1')
		self.assertEqual(voo_1_up.rota, 'SaoPauloRio')

	def test_update_specific(self):
		voo_1 =  Voo.objects.get(codigo='GOL1')
		voo_1.rota = 'Não importa'
		voo_1.companhia = 'Não importa'
		voo_1.previsao_chegada = '2016-10-25 14:30:59'
		voo_1.save(update_fields=['previsao_chegada'])

		voo_1_atrasou =  Voo.objects.get(codigo='GOL1')
		self.assertEqual(voo_1_atrasou.companhia, 'GOL')
		self.assertEqual(voo_1_atrasou.previsao_chegada,'2016-10-25 14:30:59')

	def test_delete(self):
		estado_3 = Estado_Dinamico.objects.get(codigo='TRAVE1')
		estado_3.delete()
		estado_del = Estado_Dinamico.objects.get(codigo='TRAVE1')
		self.assertIsNone(estado_del)
