from django.shortcuts import render

# Create your views here.
def login(request):
        return render(request, "login.html")

def home(request):
    return render(request,'home.html')

def cadastrar(request):
    return render(request,'cadastrar.html')

def central(request):
    return render(request, 'central.html')

def monitorar(request):
    return render(request, 'monitorar.html')

def relatorio(request):
    return render(request, 'relatorio.html')