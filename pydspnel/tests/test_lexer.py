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

    tokens = [tk.name for tk in lexer.lex("in a: <u32>")]
    assert(tokens == ['IN', 'IDENTIFIER', 'DDOTS', 'LT', 'IDENTIFIER', 'GT'])

def test_assign():
    tokens = [tk.name for tk in lexer.lex("let DFT_4_kernel = DFT_4.foo();")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'IDENTIFIER', 'DOT', 'IDENTIFIER', 'OPEN_PARENS', 'CLOSE_PARENS', 'SEMICOLON'])

    tokens = [tk.name for tk in lexer.lex("let DFT_4_kernel = DFT_4.kernel();")]
    assert(tokens == ['LET', 'IDENTIFIER', 'EQUALS', 'IDENTIFIER', 'DOT', 'KERNEL', 'OPEN_PARENS', 'CLOSE_PARENS', 'SEMICOLON'])
