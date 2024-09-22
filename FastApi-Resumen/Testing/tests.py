import pytest 

# Ejemplo 
def add(a:int,b:int) -> int:
    return a + b


@pytest.mark.parametrize('a,b,result',[(2,3,5),(0,0,0),(100,0,100)])
def test_add(a:int,b:int,result:int) -> None:
    assert add(a,b) == result
