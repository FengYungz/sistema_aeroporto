import csv
import dbm
import pkgutil
import sqlite3

from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import Login, CadastrarVoo, MonitorarVoo
from .models import Voo, Estado_Dinamico, Funcionario
from .filters import FiltroCentral, FiltroMonitorar

def login(request, context = {}):
    form = Login()
    context={}
    
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
                        request.session['tentativas'] = 0
                        request.session['permisao'] = funcionario.cargo
                        print(request.session['permisao'])
                        return redirect('home')
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

def edit(request,id):
    request.session['tentativas'] = 0

    voo = Voo.objects.get(id = id)
    form = CadastrarVoo(instance=voo)
    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = CadastrarVoo(request.POST,instance=voo)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('central')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form}
        return render(request,'central.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form}
    return render(request,'central.html',context)

def deletar(request,id):
    request.session['tentativas'] = 0

    Voo.objects.filter(id = id).delete()
    
    return redirect('central')

def home(request, context = {'permisao':'Negada'}):
    request.session['tentativas'] = 0
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos_dinamico':voos_dinamico}
    
    return render(request,'home.html',context)

def cadastrar(request):
    request.session['tentativas'] = 0
    form = CadastrarVoo(request.POST)
    context={'form':form}
    if request.method == "POST":
        if form.is_valid():
            print("cadastro")
            post = form.save(commit=False)
            post.save()
            Estado_Dinamico.objects.create(voo = post , status= 'EMB', data_saida ='1111-01-01 00:00', data_chegada ='1111-01-01 01:01')
        return redirect('cadastrar')
    return render(request,'cadastrar.html',context)

def central(request):
    request.session['tentativas'] = 0

    voos=Estado_Dinamico.objects.all()
    filter = FiltroCentral(request.GET, queryset=voos)
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos_dinamico':voos_dinamico,'estado':'listar','filter':filter}
    return render(request, 'central.html',context)

def monitorar(request):
    request.session['tentativas'] = 0
    form = MonitorarVoo(request.POST)
    voos_dinamico = Estado_Dinamico.objects.select_related()

    voos = Estado_Dinamico.objects.all()
    filter = FiltroMonitorar(request.GET, queryset=voos)
    
    context={'voos_dinamico':voos_dinamico,'estado' : 'listagem','form':form,'filter':filter}
    
    return render(request, 'monitorar.html',context)

def monitoramento(request,id):
    request.session['tentativas'] = 0

    voo = Voo.objects.get(id = id)
    estado = Estado_Dinamico.objects.get(voo = voo)
    form = MonitorarVoo(instance=estado)

    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = MonitorarVoo(request.POST,instance=estado)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('monitorar')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form}
        return render(request,'monitorar.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form}
    return render(request,'monitorar.html',context)

def relatorio(request):
    request.session['tentativas'] = 0
    # Listagem ainda não implementada no front
    voos=Voo.objects.all()
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos':voos,'voos_dinamico':voos_dinamico}
    return render(request, 'relatorio.html',context)

# pravavelmente não vai usar
def editar_voo(request):
    request.session['tentativas'] = 0
    form = CadastrarVoo(request.POST)
    voo_edit = request.POST['codigos']
    post = Voo.objects.filter(codigo = voo_edit)
    context={'form':form}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    return redirect('central')

def relatorio1(request):
    request.session['tentativas'] = 0
    response = HttpResponse(content_type='text.csv')
    response['Content-Disposition'] = 'attachment; filename="voos.csv"'

    writer = csv.writer(response)
    writer.writerow(['codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota'])
 
    voos_cadastrados = Voo.objects.all().values_list('codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')
    for user in voos_cadastrados:
        writer.writerow(user)
 
    return response

def relatorio2(request):
    request.session['tentativas'] = 0
    response = HttpResponse(content_type='text.csv')
    response['Content-Disposition'] = 'attachment; filename="voos.csv"'

    writer = csv.writer(response)
    writer.writerow(['codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota'])
 
    voos_cadastrados = Voo.objects.all().values_list('codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')
    for user in voos_cadastrados:
        writer.writerow(user)
 
    return response




