from django.conf import settings
from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone
import datetime


#exemplo de instrucoes
# Produto.objects.filter(idproduto=x)
# Post.objects.filter(title__contains='title')
# Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

class Voo(models.Model):
	STATUS = [
		('GOL', 'Gol'),
		('TAM', 'TAM '),
		('AVC', 'Avianca '),
		('AZL', 'Azul '),
		# adicionar mais estados aqui abaixo
	]

	id = models.BigAutoField(primary_key=True)

	codigo = models.CharField(max_length=12, null=False,unique = True)
	companhia = models.CharField(max_length=3,choices=STATUS, null=False)
	
	previsao_chegada = models.DateTimeField(null=False)
	previsao_partida = models.DateTimeField(null=False)

	rota = models.CharField(max_length=200, null=False)

	class Meta:
		db_table = 'Voos'

class Estado_Dinamico(models.Model):
	voo = models.OneToOneField(
        Voo,
        on_delete=models.CASCADE,
        primary_key=True,
    )

	STATUS = [
		('EMB', 'Embarque'),
		('PSO', 'Pouso'),
		('DEC', 'Decolagem'),
		('FIN', 'Finalizado'),
		# adicionar mais estados aqui abaixo
	]

	data_saida = models.DateTimeField(blank=True)
	data_chegada = models.DateTimeField(blank=True)
	
	status = models.CharField(max_length=3,choices=STATUS,default = 'EMB')

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


