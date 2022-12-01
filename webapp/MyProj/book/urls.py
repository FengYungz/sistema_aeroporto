from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name = 'login'),
    path('home/', views.home, name='home'),

    # CRUD 
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('central/', views.central, name = 'central'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('deletar/<int:id>', views.deletar, name='deletar'),

    # Monitorar
    path('monitorar/', views.monitorar, name = 'monitorar'),
    path('monitoramento/chegada/<int:id>', views.monitoramento, name = 'monitoramento'),
    path('monitoramento/saida/<int:id>', views.monitoramento2, name = 'monitoramento2'),

     # Relatorio
    path('relatorio/', views.relatorio, name = 'relatorio'),
    path('relatorio1/', views.relatorio1, name = 'relatorio1'),
    path('relatorio1/completo/', views.relatorio1all, name = 'relatorio1all'),
    path('relatorio2/', views.relatorio2, name = 'relatorio2'),
    path('relatorio2/completo/', views.relatorio2all, name = 'relatorio2all'),


    path('erro/', views.erro, name = 'erro')
]