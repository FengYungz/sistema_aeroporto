from django.conf import settings
from django.db import models
from django.utils import timezone

#exemplo de instrucoes
# Produto.objects.filter(idproduto=x)
# Post.objects.filter(title__contains='title')
# Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

class Voo(models.Model):
	id = models.BigAutoField(primary_key=True)

	codigo = models.CharField(max_length=12, null=False, unique=True)
	companhia = models.CharField(max_length=150, null=False)
	
	previsao_chegada = models.DateTimeField(null=False)
	previsao_partida = models.DateTimeField(null=False)
	
	data_chegada = models.DateTimeField( blank=True)
	data_saida = models.DateTimeField( blank=True)

	status = models.CharField(max_length=20)
	
	rota = models.CharField(max_length=200, null=False)

	class Meta:
		db_table = 'Voos'



class Funcionario(models.Model):
	id = models.BigAutoField(primary_key=True)
	nome = models.CharField(max_length=200)
	cpf = models.CharField(max_length=11)
	cargo = models.CharField(max_length=200)

	class Meta:
		db_table = 'Funcionarios'


