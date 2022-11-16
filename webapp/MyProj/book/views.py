import csv
import dbm
from multiprocessing import context
import pkgutil
import sqlite3
from turtle import pd
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import Login, CadastrarVoo, MonitorarVoo
from django.utils import timezone
from .models import Voo, Estado_Dinamico, Funcionario

from django.http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.
def login(request, context = {}):
    form = Login()
    
    if 'tentativas' in request.session:
        tentativas = request.session['tentativas']
        request.session['tentativas'] = tentativas + 1
    else:
        request.session['tentativas'] = 0

    print(request.session['tentativas'])

    if request.method == "POST":
        if tentativas < 3:
            form = Login(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    funcionario = Funcionario.objects.get(cpf = post.cpf)
                except Funcionario.DoesNotExist:
                    funcionario = None
                if funcionario is not None:
                    if(post.senha == funcionario.senha):
                        context = {'permisao':funcionario.cargo}
                        return render(request,'home.html',context)
                    else:
                        context={'form':form, 'mensagem':'Senha incorreta','estado':200}
                        return render(request, 'login.html', context)
                else:
                    context={'form':form, 'mensagem':'Funcionario não cadastrado','estado':200}
                    return render(request, 'login.html', context)
        else:
            context={'form':form, 'mensagem':'Tentativas exedidas', 'estado':400}
            return render(request, 'login.html', context)
    else:
        form = Login()
        context={'form':form,'estado':200}
    return render(request, 'login.html', context)


def home(request):
    #EstadoDinamicoLista = Estado_Dinamico.objects.get
    all_entries = Estado_Dinamico.objects.all()
       
    return render(request,'home.html')

def home(request, context = {'permisao':'Negada'}):
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos_dinamico':voos_dinamico}
    
    return render(request,'home.html',context)

def cadastrar(request):
    form = CadastrarVoo(request.POST)
    context={'form':form}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            estado = Estado_Dinamico.objects.create(voo = post , status= 'EMB', data_saida ='0001-01-01 00:00', data_chegada ='0001-01-01 01:01')
        return redirect('cadastrar')
    return render(request,'cadastrar.html',context)


def central(request):
    # Listagem ainda não implementada no front
    filter = {}
    voos=Voo.objects.all()
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos_dinamico':voos_dinamico}
    return render(request, 'central.html',context)

def monitorar(request):
    form = MonitorarVoo()
    voos = Estado_Dinamico.objects.select_related()
    context={'form':form,'voos':voos}
    if request.method == "POST":
        form = MonitorarVoo(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            voo_dinamico = get_object_or_404(Estado_Dinamico, codigo = post.codigo)
            voo_dinamico = post
            voo_dinamico.save()
            return redirect('monitorar')
    return render(request, 'monitorar.html',context)

def relatorio(request):
    # Listagem ainda não implementada no front
    voos=Voo.objects.all()
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos':voos,'voos_dinamico':voos_dinamico}
    return render(request, 'relatorio.html',context)

def editar_voo(request):
    form = CadastrarVoo(request.POST)
    voo_edit = request.POST['codigos']
    post = Voo.objects.filter(codigo = voo_edit)
    context={'form':form}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    return redirect('central')

def relatorio(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voos.csv"'
 
    writer = csv.writer(response)
    writer.writerow(['codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota'])
 
    voos_cadastrados = Voo.objects.all().values_list('codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')
    for user in voos_cadastrados:
        writer.writerow(user)
 
    return response



