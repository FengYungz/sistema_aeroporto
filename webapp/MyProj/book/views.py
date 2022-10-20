from multiprocessing import context
import pkgutil
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import Login, CadastrarVoo
from django.utils import timezone
from .models import Voo, Estado_Dinamico, Funcionario


# Create your views here.
def login(request):
        return render(request, "login.html")

def home(request):
    return render(request,'home.html')

def cadastrar(request):
    novoVoo = get_object_or_404(Voo, pk=pkgutil)
    if request.method == "POST":
        form = CadastrarVoo(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.data = timezone.now()
            post.save()
            novoVoo.save()
    return render(request,'cadastrar.html')

def central(request):
    return render(request, 'central.html')

def monitorar(request):
    return render(request, 'monitorar.html')

def relatorio(request):
    return render(request, 'relatorio.html')