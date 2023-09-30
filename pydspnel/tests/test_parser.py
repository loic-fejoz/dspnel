from pydspnel import parse

def test_number():
    ast = parse('3')
    ast = ast.asLisp()
    assert ast == '3'

    ast = parse('3.2')
    ast = ast.asLisp()
    assert ast == '3.2'

    ast = parse('3e-2')
    ast = ast.asLisp()
    assert ast == '3e-2'

    ast = parse('3j')
    ast = ast.asLisp()
    assert ast == '3j'

def test_arith():
    ast = parse('3 + 2')
    ast = ast.asLisp()
    assert ast == '(Add 3 2)'

    ast = parse('3 + 2 * 5')
    ast = ast.asLisp()
    assert ast == '(Add 3 (Mul 2 5))'

    ast = parse('3 * 2 + 5')
    ast = ast.asLisp()
    assert ast == '(Add (Mul 3 2) 5)'

    ast = parse('3 + 2j')
    ast = ast.asLisp()
    assert ast == '(Add 3 2j)'

def test_matrix():
    ast = parse('[2, 3]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2 3))'

    ast = parse('[2, 4; 3, 5]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2 4) (Row 3 5))'

    ast = parse('[2; 5]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2) (Row 5))'

    ast = parse('[2*k for k in 0..10]')
    ast = ast.asLisp()
    assert ast == '(Matrix (RowIter (Mul 2 k) k 0 10))'

    ast = parse('[2*k for k in 0..10].conj()')
    ast = ast.asLisp()
    assert ast == '(MethodCall conj (Matrix (RowIter (Mul 2 k) k 0 10)) ())'