from django.conf import settings
from django.db import models
from django.utils import timezone

#exemplo de instrucoes
# Produto.objects.filter(idproduto=x)
# Post.objects.filter(title__contains='title')
# Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

class Voo(models.Model):
	companhia = models.CharField(max_length=50)
	codigo = models.PositiveIntegerField()
	
	previsao_saida = models.DateTimeField()
	previsao_chegada = models.DateTimeField()
	
	real_saida = models.DateTimeField()
	real_chegada = models.DateTimeField()

	rota = models.CharField(max_length=200)

	aeroporto_chegada = models.CharField(max_length=200)
	aeroporto_saida = models.CharField(max_length=200)
	status = models.CharField(max_length=200)




	def publish(self):
		self.data = timezone.now()
		self.save()

	def __str__(self):
		return self.nome


class Funcionario(models.Model):
	nome = models.CharField(max_length=200)
	cpf = models.CharField(max_length=11)
	cargo = models.CharField(max_length=200)

	def publish(self):
		self.save()

	def __str__(self):
		return self.nome


