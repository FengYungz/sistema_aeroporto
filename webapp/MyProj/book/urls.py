from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name = 'login'),
    path('home/', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('central/', views.central, name = 'central'),
    path('monitorar/', views.monitorar, name = 'monitorar'),
    path('relatorio/', views.relatorio, name = 'relatorio')
]