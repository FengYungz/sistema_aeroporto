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
    path('monitoramento/<int:id>', views.monitoramento, name = 'monitoramento'),

    # Relatorio
    path('relatorio/', views.relatorio, name = 'relatorio'),
    path('relatorio1/', views.relatorio1, name = 'relatorio1'),
    path('relatorio2/', views.relatorio2, name = 'relatorio2')
]