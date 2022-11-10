from multiprocessing import context
import pkgutil
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import Login, CadastrarVoo, MonitorarVoo
from django.utils import timezone
from .models import Voo, Estado_Dinamico, Funcionario


# Create your views here.
def login(request, context = {}):
    form = Login()
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                funcionario = Funcionario.objects.get(cpf = post.cpf)
            except Funcionario.DoesNotExist:
                funcionario = None
            if funcionario is not None:
                if(post.senha == funcionario.senha):
                #     return redirect('home')
                    # quando o front estiver sendo feito:
                    permisao = {'permisao':funcionario.cargo}
                    return render(request,'home.html',permisao)
                else:
                    context={'form':form, 'mensagem':'Senha incorreta'}
                    return render(request, 'login.html', context)
            else:
                context={'form':form, 'mensagem':'Funcionario não cadastrado'}
                return render(request, 'login.html', context)
    else:
        form = Login()
        context={'form':form}
    return render(request, 'login.html', context)

def home(request, permisao):
    return render(request,'home.html',permisao)

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
    context={'voos':voos,'voos_dinamico':voos_dinamico}
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



# funcoes adicionais
def deletar(request):
    voos_del = request.POST['codigos']
    voos_del = voos_del.split(",")
    voos = Voo.objects.filter(codigo = voos_del)
    voos.delete()
    return redirect('central')


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