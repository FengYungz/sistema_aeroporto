from django.conf import settings
from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone
import datetime

class Voo(models.Model):
	STATUS = [
		('GOL', 'Gol'),
		('TAM', 'TAM '),
		('AVC', 'Avianca '),
		('AZL', 'Azul '),
		# adicionar mais estados aqui abaixo
	]

	ROTAS = [
		('11-22', '11-22'),
		('22-11', '22-11'),
		('11-33', '11-33'),
		('44-11', '44-11'),
		# adicionar mais estados aqui abaixo
	]

	id = models.BigAutoField(primary_key=True)

	codigo = models.CharField(max_length=12, null=False,unique = True)
	companhia = models.CharField(max_length=3,choices=STATUS, null=False)
	
	previsao_chegada = models.DateTimeField(null=False)
	previsao_partida = models.DateTimeField(null=False)

	rota = models.CharField(max_length=5,choices=ROTAS, null=False)

	class Meta:
		db_table = 'Voos'

class Estado_Dinamico(models.Model):
	voo = models.OneToOneField(
        Voo,
        on_delete=models.CASCADE,
        primary_key=True,
    )

	STATUS = [
		('Embarque', 'Embarque'),
		('Pouso', 'Pouso'),
		('Decolagem', 'Decolagem'),
		('Finalizado', 'Finalizado'),
		('Espera', 'Espera'),
		# adicionar mais estados aqui abaixo
	]

	data_saida = models.DateTimeField(null=True)
	data_chegada = models.DateTimeField(null=True)
	
	status = models.CharField(max_length=10,choices=STATUS,default = 'EMB')

	class Meta:
			db_table = 'estado_dinamico'


class Funcionario(models.Model):
	id = models.BigAutoField(primary_key=True)
	senha  = models.CharField(max_length=20, null=False)
	nome = models.CharField(max_length=200)
	cpf = models.CharField(max_length=11)
	cargo = models.CharField(max_length=200)

	class Meta:
		db_table = 'Funcionarios'