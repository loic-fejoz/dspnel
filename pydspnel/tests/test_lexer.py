from pydspnel.lexer import lexer

def test_numbers_assign():
    tokens = [tk.name for tk in lexer.lex("let a = 3.0;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = 3;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = 3e-6;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = 5j;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = 4e2i;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let in_degrees = 360.0 * a;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'MUL', 'IDENTIFIER', 'SEMICOLON'])

def test_vector_matrix_assign():
    tokens = [tk.name for tk in lexer.lex("let a = [4, 2];")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS',
                      'OPEN_SQBRACKET',
                      'NUMBER', 'COMMA', 'NUMBER',
                      'CLOSE_SQBRACKET',
                      'SEMICOLON'])
    
    tokens = [tk.name for tk in lexer.lex("let a = [4, 2; 3, 5];")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS',
                      'OPEN_SQBRACKET',
                      'NUMBER', 'COMMA', 'NUMBER', 'SEMICOLON',
                      'NUMBER', 'COMMA', 'NUMBER',
                      'CLOSE_SQBRACKET',
                      'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = [[4, 2], [3, 5]];")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS',
                      'OPEN_SQBRACKET', 'OPEN_SQBRACKET',
                      'NUMBER', 'COMMA', 'NUMBER', 'CLOSE_SQBRACKET', 'COMMA',
                      'OPEN_SQBRACKET', 'NUMBER', 'COMMA', 'NUMBER', 'CLOSE_SQBRACKET',
                      'CLOSE_SQBRACKET',
                      'SEMICOLON'])
    

    tokens = [tk.name for tk in lexer.lex('[2*k for k in 0..10]')]
    assert(tokens == ['OPEN_SQBRACKET', 'NUMBER', 'MUL', 'IDENTIFIER', 'FOR', 'IDENTIFIER', 'IN', 'NUMBER', 'RANGE', 'NUMBER', 'CLOSE_SQBRACKET'])
    
def test_numbers_typed_assign():
    tokens = [tk.name for tk in lexer.lex("let a: u32 = 3.0;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'DDOTS', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a = 3.0;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'NUMBER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let a: u32;")]
    assert(tokens == ['LET', 'IDENTIFIER', 'DDOTS', 'IDENTIFIER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("in a: <u32>")]
    assert(tokens == ['IN', 'IDENTIFIER', 'DDOTS', 'LT', 'IDENTIFIER', 'GT'])

def test_assign():
    tokens = [tk.name for tk in lexer.lex("let DFT_4_kernel = DFT_4.foo();")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'IDENTIFIER', 'DOT', 'IDENTIFIER', 'OPEN_PARENS', 'CLOSE_PARENS', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("a = 3 * a;")]
    assert(tokens == ['IDENTIFIER', 'EQUALS', 'NUMBER', 'MUL', 'IDENTIFIER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("a *= 3 + b;")]
    assert(tokens == ['IDENTIFIER', 'MUL_ASSIGN', 'NUMBER', 'PLUS', 'IDENTIFIER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("a -= 3 + b;")]
    assert(tokens == ['IDENTIFIER', 'SUB_ASSIGN', 'NUMBER', 'PLUS', 'IDENTIFIER', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("a += 3 + b;")]
    assert(tokens == ['IDENTIFIER', 'ADD_ASSIGN', 'NUMBER', 'PLUS', 'IDENTIFIER', 'SEMICOLON'])

def test_expr():
    tokens = [tk.name for tk in lexer.lex("a.b.foo()")]
    assert(tokens == ['IDENTIFIER', 'DOT', 'IDENTIFIER', 'DOT', 'IDENTIFIER', 'OPEN_PARENS', 'CLOSE_PARENS'])

    tokens = [tk.name for tk in lexer.lex("a.b.foo(arg1: c)")]
    assert(tokens == ['IDENTIFIER', 'DOT', 'IDENTIFIER', 'DOT', 'IDENTIFIER', 'OPEN_PARENS', 'IDENTIFIER', 'DDOTS', 'IDENTIFIER', 'CLOSE_PARENS'])

    tokens = [tk.name for tk in lexer.lex("if a { b } else { c }")]
    assert(tokens == ['IF', 'IDENTIFIER', 'OPEN_BRACKETS', 'IDENTIFIER', 'CLOSE_BRACKETS', 'ELSE', 'OPEN_BRACKETS', 'IDENTIFIER', 'CLOSE_BRACKETS'])

    tokens = [tk.name for tk in lexer.lex("a < b")]
    assert(tokens == ['IDENTIFIER', 'LT', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a <= b")]
    assert(tokens == ['IDENTIFIER', 'LEQ', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a > b")]
    assert(tokens == ['IDENTIFIER', 'GT', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a >= b")]
    assert(tokens == ['IDENTIFIER', 'GEQ', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a and b")]
    assert(tokens == ['IDENTIFIER', 'AND', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a or b")]
    assert(tokens == ['IDENTIFIER', 'OR', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a xor b")]
    assert(tokens == ['IDENTIFIER', 'XOR', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("not b")]
    assert(tokens == ['NOT', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a == b")]
    assert(tokens == ['IDENTIFIER', 'DEQUALS', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a != b")]
    assert(tokens == ['IDENTIFIER', 'DIFFERENT', 'IDENTIFIER'])

    tokens = [tk.name for tk in lexer.lex("a ==> b")]
    assert(tokens == ['IDENTIFIER', 'IMPLY', 'IDENTIFIER'])


def test_kernel():
    tokens = [tk.name for tk in lexer.lex("kernel A(){}")]
    assert(tokens == ['KERNEL', 'IDENTIFIER', 'OPEN_PARENS', 'CLOSE_PARENS', 'OPEN_BRACKETS', 'CLOSE_BRACKETS'])

    tokens = [tk.name for tk in lexer.lex("let DFT_4_kernel = DFT_4.kernel();")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'IDENTIFIER', 'DOT', 'IDENTIFIER', 'OPEN_PARENS', 'CLOSE_PARENS', 'SEMICOLON'])
