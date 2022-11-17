import django_filters

from .models import Voo, Estado_Dinamico, Funcionario


class FiltroCentral(django_filters.FilterSet):
    voo__codigo = django_filters.CharFilter(lookup_expr='icontains',label='Codigo')
    voo__companhia = django_filters.CharFilter(lookup_expr='icontains',label='Companhia')
    voo__previsao_chegada = django_filters.DateTimeFilter(lookup_expr='icontains',label='Previsao de Chegada')
    voo__previsao_partida = django_filters.DateTimeFilter(lookup_expr='icontains',label='Previsao de Partida')
    voo__rota = django_filters.CharFilter(lookup_expr='icontains',label='Rota')

    status = django_filters.CharFilter(lookup_expr='icontains',label='Status')

    class Meta:
        model = Estado_Dinamico
        fields = ['voo__codigo', 'voo__companhia', 'voo__previsao_chegada', 'voo__previsao_partida', 'voo__rota', 'status']

        #         fields = {
        #     'voo__codigo':['Codigo','icontains'],
        #     'voo__companhia':['Codigo','icontains'],
        #     'voo__previsao_chegada':['Codigo','icontains'],
        #     'voo__previsao_partida':['Codigo','icontains'],
        #     'voo__rota':['Codigo','icontains'],
        #     'status':['Codigo','icontains']
        # }


class FiltroMonitorar(django_filters.FilterSet):
    voo__codigo = django_filters.CharFilter(lookup_expr='icontains',label='Codigo')
    voo__companhia = django_filters.CharFilter(lookup_expr='icontains',label='Companhia')
    data_saida = django_filters.DateTimeFilter(lookup_expr='icontains',label='Data de Chegada')
    data_chegada = django_filters.DateTimeFilter(lookup_expr='icontains',label='Data de Partida')
    voo__rota = django_filters.CharFilter(lookup_expr='icontains',label='Rota')

    status = django_filters.CharFilter(lookup_expr='icontains',label='Status')

    class Meta:
        model = Estado_Dinamico
        fields = ['voo__codigo', 'voo__companhia', 'data_saida', 'data_chegada', 'voo__rota', 'status']