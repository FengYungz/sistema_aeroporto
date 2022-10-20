from django import forms

from  .models import Voo,Estado_Dinamico,Funcionario


class Login(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ('cpf', 'senha')

class CadastrarVoo(forms.ModelForm):

    class Meta:
        model = Voo
        fields = ('codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')