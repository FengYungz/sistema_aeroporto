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

from .forms import Login, CadastrarVoo, MonitorarVoo,MonitorarVoo2,EditarVoo
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
                        request.session['permissao'] = funcionario.cargo
                        print(request.session['permissao'])
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
    permissao = request.session['permissao']
    request.session['tentativas'] = 0

    voo = Voo.objects.get(id = id)
    form = EditarVoo(request.POST or None,instance=voo)
    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = EditarVoo(request.POST or None,instance=voo)
        if form.is_valid():
            
            post = form.save(commit=False)
            if post.previsao_partida > post.previsao_chegada:
                return erro(request,'Erro: previsao de chegada menor que a de saida ')
            post.save()
            return redirect('central')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'mensagem': voo.codigo,'permissao':permissao}
        return render(request,'central.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'mensagem': voo.codigo,'permissao':permissao}
    return render(request,'central.html',context)

def deletar(request,id):
    request.session['tentativas'] = 0

    Voo.objects.filter(id = id).delete()
    
    return redirect('central')

def home(request, context = {'permissao':'Negada'}):
    request.session['tentativas'] = 0
    permissao = request.session['permissao']
    voos_dinamico = Estado_Dinamico.objects.select_related().order_by('-voo__previsao_partida')[:10]
    context={'voos_dinamico':voos_dinamico,'permissao':permissao}
    
    return render(request,'home.html',context)

def cadastrar(request):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0
    form = CadastrarVoo(request.POST or None)
    context={'form':form,'permissao':permissao}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            if post.previsao_partida > post.previsao_chegada:
                return erro(request,'Erro: previsao de chegada menor que a de saida ')
            post.save()
            Estado_Dinamico.objects.create(voo = post , status= 'Espera')
        return redirect('cadastrar')
    return render(request,'cadastrar.html',context)

def central(request):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0

    voos=Estado_Dinamico.objects.all()
    filter = FiltroCentral(request.GET, queryset=voos)
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos_dinamico':voos_dinamico,'estado':'listar','filter':filter,'permissao':permissao}
    return render(request, 'central.html',context)

def monitorar(request):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0
    form = MonitorarVoo(request.POST or None)
    voos_dinamico = Estado_Dinamico.objects.select_related()

    voos = Estado_Dinamico.objects.all()
    filter = FiltroMonitorar(request.GET, queryset=voos)
    
    context={'voos_dinamico':voos_dinamico,'estado' : 'listagem','form':form,'filter':filter,'permissao':permissao}
    
    return render(request, 'monitorar.html',context)

def monitoramento2(request,id):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0

    voo = Voo.objects.get(id = id)
    estado = Estado_Dinamico.objects.get(voo = voo)
    estadocompare = Estado_Dinamico.objects.get(voo = voo)
    form = MonitorarVoo(request.POST or None,instance=estado)

    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = MonitorarVoo(request.POST,instance=estado)
        if form.is_valid():
            post = form
            if post.cleaned_data['status'] == 'Pouso' or post.cleaned_data['status'] == 'Finalizado':
                return erro(request,'Esta operação não pode ser realizada, utilize a opção "Editar Chegada"')
            if post.cleaned_data['status'] !=  estadocompare.status :
                if (post.cleaned_data['status'] == 'Embarque' and estadocompare.status != 'Espera') or (post.cleaned_data['status'] == 'Decolagem' and estadocompare.status != 'Embarque') or (post.cleaned_data['status'] == 'Pouso' and estadocompare.status != 'Decolagem') or (post.cleaned_data['status'] == 'Finalizado' and estadocompare.status != 'Pouso'):
                    return erro(request,'Erro: ordem de operação incorreta: de '+estadocompare.status+' para '+ post.cleaned_data['status'])
            post.save()
            return redirect('monitorar')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'permissao':permissao}
        return render(request,'monitorar.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'permissao':permissao}
    return render(request,'monitorar.html',context)


def monitoramento(request,id):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0

    voo = Voo.objects.get(id = id)
    estado = Estado_Dinamico.objects.get(voo = voo)
    estadocompare = Estado_Dinamico.objects.get(voo = voo)
    form = MonitorarVoo2(request.POST or None,instance=estado)

    voos_dinamico = Estado_Dinamico.objects.select_related()
    
    if request.method == "POST":
        form = MonitorarVoo2(request.POST,instance=estado)
        if form.is_valid():
            post = form
            if post.cleaned_data['status'] != 'Pouso' or post.cleaned_data['status'] != 'Finalizado':
                return erro(request,'Esta operação não pode ser realizada, utilize a opção "Editar Saida"')
            if post.cleaned_data['status'] !=  estadocompare.status :
                if (post.cleaned_data['status'] == 'Embarque' and estadocompare.status != 'Espera') or (post.cleaned_data['status'] == 'Decolagem' and estadocompare.status != 'Embarque') or (post.cleaned_data['status'] == 'Pouso' and estadocompare.status != 'Decolagem') or (post.cleaned_data['status'] == 'Finalizado' and estadocompare.status != 'Pouso'):
                    return erro(request,'Erro: ordem de operação incorreta: de '+estadocompare.status+' para '+ post.cleaned_data['status'])
            if estadocompare.data_saida is None:
                return erro(request,'Este voo ainda não partiu')
            if post.cleaned_data['data_chegada'] is not None:
                if estadocompare.data_saida > post.cleaned_data['data_chegada']:
                    return erro(request,'Erro: data de chegada menor que a de saida ')
            post.save()
            return redirect('monitorar')

        context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'permissao':permissao}
        return render(request,'monitorar.html',context)

    context={'voos_dinamico':voos_dinamico,'estado':'edicao','form':form,'permissao':permissao}
    return render(request,'monitorar.html',context)

def relatorio(request):
    permissao = request.session['permissao']
    request.session['tentativas'] = 0
    # Listagem ainda não implementada no front
    voos=Voo.objects.all()
    voos_dinamico = Estado_Dinamico.objects.select_related()
    context={'voos':voos,'voos_dinamico':voos_dinamico,'permissao':permissao}
    return render(request, 'relatorio.html',context)



def relatorio1(request):
    result = Voo.objects.select_related().values()             
    list_result = [entry for entry in result]
    
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(180, 10, 'Voos Cadastrados',ln=2, align='C')
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 8, f"{'Código'}      {'Companhia'}       {'Previsão_chegada'}                         {'Previsão_partida'}                       {'Rota'}", 0, 1, 2, 3)
    pdf.line(10, 30, 200, 30)
    pdf.line(10, 38, 200, 38)

    for line in list_result:
        pdf.cell(200, 8, f"{line['codigo']}          {line['companhia']}          {line['previsao_chegada']}          {line['previsao_partida']}          {line['rota']}", 0, 1, 2, 3)
    pdf.output('report.pdf', 'F')

    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')    

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



