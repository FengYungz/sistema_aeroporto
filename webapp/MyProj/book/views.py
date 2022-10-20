from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Login
# Create your views here.
def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            funcionario = get_object_or_404(Funcionario, cpf = post.cpf)
            if(post.senha == post.funcionario.senha):
                return redirect('home')
            else:
                return redirect('login')
    else:
        form = CriaVenda()
        context={'form':form}
    return render(request, 'login.html')

def home(request):
    return render(request,'home.html')

def cadastrar(request):
    return render(request,'cadastrar.html')

def central(request):
    return render(request,'central.html')

def monitorar(request):
    return render(request,'monitorar.html')

def relatorio(request):
    return render(request,'relatorio.html')