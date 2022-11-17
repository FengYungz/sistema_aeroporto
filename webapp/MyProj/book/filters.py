import django_filters

from .models import Voo, Estado_Dinamico, Funcionario


class FiltroCentral(django_filters.FilterSet):
    codigo = django_filters.CharFilter(lookup_expr='icontains',label='Codigo')
    companhia = django_filters.CharFilter(lookup_expr='icontains',label='Companhia')
    previsao_chegada = django_filters.DateTimeFilter(lookup_expr='icontains',label='Previsao de Chegada')
    previsao_partida = django_filters.DateTimeFilter(lookup_expr='icontains',label='Previsao de Partida')
    rota = django_filters.CharFilter(lookup_expr='icontains',label='Rota')

    status = django_filters.CharFilter(lookup_expr='icontains',label='Status')

    class Meta:
        model = Estado_Dinamico
        fields = ['codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota', 'status']