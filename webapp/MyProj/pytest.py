import pytest
from book.models import Voo, Estado_Dinamico, Funcionario

def test_1():
    voos = Voo.objects.all()
    
    assert voos == Voo.objects.all()