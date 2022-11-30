import csv
import dbm
import io
import pkgutil
import sqlite3
import pdfkit
import pandas as pd 

from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from fpdf import FPDF
from reportlab.pdfgen import canvas
from django.http import FileResponse

from .forms import Login, CadastrarVoo, MonitorarVoo,EditarVoo
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
    form = EditarVoo(instance=voo)
    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = CadastrarVoo(request.POST,instance=voo)
        if form.is_valid():
            
            post = form.save(commit=False)
            if post.previsao_partida > post.previsao_chegada:
                return erro(request,'Erro: previsao de chegada menor que a de saida ')
            post.save()
            return redirect('central')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'mensagem': voo.codigo}
        return render(request,'central.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'mensagem': voo.codigo}
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
            post = form.save(commit=False)
            if post.previsao_partida > post.previsao_chegada:
                return erro(request,'Erro: previsao de chegada menor que a de saida ')
            post.save()
            Estado_Dinamico.objects.create(voo = post , status= 'Nda')
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
            if post.data_chegada is not None:
                if post.data_saida > post.data_chegada:
                    return erro(request,'Erro: data de chegada menor que a de saida ')
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
    result = Estado_Dinamico.objects.select_related().values()          
    list_result = [entry for entry in result]
    
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(180, 10, 'Estado dos Voos Cadastrados', ln=2, align='C')
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 8, f"{'Código'}              {'Data_saída'}                                    {'Data_chegada'}                          {'Status'}", 0, 2, 4, 6)
    pdf.line(10, 30, 180, 30)
    pdf.line(10, 38, 180, 38)

    for line in list_result:
        voo = Voo.objects.get(id = line['voo_id'])
        pdf.cell(200, 8, f"{voo.codigo}       {line['data_saida']}           {line['data_chegada']}              {line['status']}", 0, 2, 4, 6)
    pdf.output('report.pdf', 'F')

    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')







   
    # request.session['tentativas'] = 0
    # response = HttpResponse(content_type='text.csv')
    # response['Content-Disposition'] = 'attachment; filename="voos.csv"'

    # writer = csv.writer(response)
    # writer.writerow(['codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota'])
 
    # voos_cadastrados = Voo.objects.all().values_list('codigo', 'companhia', 'previsao_chegada', 'previsao_partida', 'rota')
    # for user in voos_cadastrados:
    #     writer.writerow(user)
 
    #return response


def erro(request,mensagem):
    context = {'mensagem':mensagem}
    return render(request, 'erro.html',context)



