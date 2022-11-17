from django import forms

from  .models import Voo,Estado_Dinamico,Funcionario


class Login(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ('cpf', 'senha')

class CadastrarVoo(forms.ModelForm):

    class Meta:
        model = Voo
        fields = ( 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')

class MonitorarVoo(forms.ModelForm):

    data_saida = forms.DateTimeField(
        label=("Data de saida"),
        required=False
    )
    data_chegada = forms.DateTimeField(
        label=("Data de chegada"),
        required=False
    )
    status = forms.CharField(
        label=("Status"),
        max_length=10
    )
    class Meta:
        model = Estado_Dinamico
        fields = ('data_saida', 'data_chegada', 'status')