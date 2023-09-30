from pydspnel import eval
from pydspnel.interpreter import DSPMatrix

def test_arith():
    res = eval('1 + 3')
    assert 4 == res
    assert type(res) == type(4)
    
    res = eval('1 + 3.0')
    assert 4.0 == res
    assert type(res) == type(4.0)

    assert 6 == eval('2 * 3')
    
    assert -1 == eval('2 - 3')

    assert complex(2, -3) == eval('2 - 3j')
    assert complex(2, -3.5) == eval('2 - 3.5j')
    assert complex(2, 1.5) == eval('2 + 1.5i')

    assert complex(-2, 0) == eval('2j * 1j')

    assert 4 == eval('12 / 3')

def test_matrix():
    assert DSPMatrix([2.0, 1.0]) == eval("[2.0, 1.0]")
    assert DSPMatrix([[2.0, 3.5], [1.0, 4.5]]) == eval("[2.0, 3.5; 1.0, 4.5]")
    assert DSPMatrix([[2.0], [1.0]]) == eval("[2.0; 1.0]")
    assert DSPMatrix([0, 2, 4]) == eval("[2*k for k in 0..3]")
    assert DSPMatrix([[0, 1, 2], [0, 2, 4]]) == eval("[[k * l for k in 0..3] for l in 1..3]")
    assert DSPMatrix([[0], [2], [4]]) == eval("[2*k for k in 0..3].transpose()")