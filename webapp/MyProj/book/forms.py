from django import forms

from  .models import Voo,Estado_Dinamico,Funcionario


class Login(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ('cpf', 'senha')

class CadastrarVoo(forms.ModelForm):

    CHOICES = Voo.STATUS
    companhia = forms.ChoiceField(choices = CHOICES,
        label=("companhia")
    )

    class Meta:
        model = Voo
        fields = ( 'codigo','companhia', 'previsao_chegada', 'previsao_partida', 'rota')

class EditarVoo(forms.ModelForm):

    previsao_partida = forms.DateTimeField(
        label=("Previsâo de saida"),
        required=False
    )
    previsao_chegada = forms.DateTimeField(
        label=("Previsâo de chegada"),
        required=False
    )
    # codigo = forms.CharField(
    #     required=False
    # )

    # companhia = forms.CharField(
    #     required=False
    # )
    # rota = forms.CharField(
    #     required=False
    # )

    class Meta:
        model = Voo
        fields = ('previsao_chegada', 'previsao_partida')

class MonitorarVoo(forms.ModelForm):

    data_saida = forms.DateTimeField(
        label=("Data de saida"),
        required=False
    )
    data_chegada = forms.DateTimeField(
        label=("Data de chegada"),
        required=False
    )

    CHOICES = Estado_Dinamico.STATUS
    status = forms.ChoiceField(choices = CHOICES,
        label=("Status")
    )
    class Meta:
        model = Estado_Dinamico
        fields = ('data_saida', 'data_chegada', 'status')