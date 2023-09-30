from rply import ParserGenerator
from pydspnel.ast import *

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV',
     'OPEN_SQBRACKET', 'CLOSE_SQBRACKET', 'COMMA',
     'SEMICOLON', 'FOR', 'IN', 'RANGE',
     'IDENTIFIER', 'DOT'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

@pg.production('expression : IDENTIFIER')
def expression_identifier(p):
    return Identifier(p[0].getstr())

@pg.production('expression : NUMBER')
def expression_number(p):
    return Number(p[0].getstr())

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(p):
    return p[1]

@pg.production('expression : OPEN_SQBRACKET rows CLOSE_SQBRACKET')
def expression_matrix(p):
    return Matrix(p[1])

@pg.production('rows : row')
def rows_singleton(p):
    return [ p[0] ]

@pg.production('rows : rows SEMICOLON row')
def rows_tail(p):
    return p[0] + [ p[2] ]


# row = expression FOR IDENTIFIER IN expression RANGE expression
#     | expression_list
#
# transformed into
#
# row = expresion_list row_remainder
# row_remainder = FOR IDENTIFIER IN expression RANGE expression
#               | empty

@pg.production('row : expression_list row_remainder')
def row_head(p):
    if p[1].__class__.__name__ == 'RowIter':
        p[1].expr = p[0][0]
        return p[1]
    else:
        return Row([ p[0] ] + p[1])

@pg.production('row_remainder : FOR IDENTIFIER IN expression RANGE expression')
@pg.production('row_remainder : ')
def row_iter(p):
    if len(p) == 0:
        return []
    return RowIter(None, Identifier(p[1].getstr()), p[3], p[5])

@pg.production('expression_list : expression')
def expression_singleton(p):
    return [ p[0] ]

@pg.production('expression_list : expression_list COMMA expression')
def expression_tail(p):
    return p[0] + [ p[2] ]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise AssertionError('Oops, this should not be possible!')

@pg.production('expression_emptylist : expression_list')
@pg.production('expression_emptylist : ')
def expression_tail(p):
    if p:
        return p
    else:
        return []

@pg.production('expression : expression DOT IDENTIFIER OPEN_PARENS expression_emptylist CLOSE_PARENS')
def expression_methodcall(p):
    return MethodCall(p[2].getstr(), p[0], p[4])

parser = pg.build()