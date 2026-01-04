from rply import ParserGenerator
from pydspnel.ast import *

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'MINUS', 'MUL', 'DIV',
     'OPEN_SQBRACKET', 'CLOSE_SQBRACKET', 'COMMA',
     'SEMICOLON', 'FOR', 'IN', 'OUT', 'RANGE',
     'IDENTIFIER', 'DOT', 'LET', 'DDOTS', 'EQUALS',
     'IF', 'ELSE', 'OPEN_BRACKETS', 'CLOSE_BRACKETS',
     'KERNEL', 'STATE', 'LT', 'GT', 'GEQ', 'LEQ', 'FUNCTION', 'RETURN',
     'REQUIRES', 'ENSURES', 'MUL_ASSIGN', 'SUB_ASSIGN', 'ADD_ASSIGN',
     'DEQUALS', 'DIFFERENT', 'IMPLY', 'XOR', 'OR', 'AND', 'NOT', 'MODULO',
     'COMMENT', 'DOCCOMMENT', 'PRIME', 'POW', 'QUICKCHECK', 'PIPE', 'PIPE_RIGHT', 'AMPERSAND',
     'BTLEFT', 'BTRIGHT', 'BITNEG', 'AT', 'FIXED_POINT_TYPE', 'MATCH', 'FAT_ARROW'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['COMMA']),
        ('left', ['IMPLY']),
        ('left', ['OR', 'XOR']),
        ('left', ['AND']),
        ('right', ['NOT']),
        ('left', ['GT', 'LT', 'DEQUALS', 'DIFFERENT', 'GEQ', 'LEQ']),
        ('left', ['PIPE', 'PIPE_RIGHT']),
        ('left', ['AMPERSAND']),
        ('left', ['BTLEFT', 'BTRIGHT']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV', 'MODULO']),
        ('right', ['BITNEG']),
        ('right', ['POW']),
        ('right', ['PRIME']),
        ('left', ['DOT']),
        ('left', ['OPEN_PARENS']),
        ('left', ['IF']),
        ('left', ['ELSE']),
        ('left', ['SEMICOLON']),
    ]
)

@pg.production('optional_stmts_list : optional_stmts_list stmt')
@pg.production('optional_stmts_list : ')
def stmts_list(p):
    if len(p) == 0:
        return []
    return p[0] + [ p[1] ]

@pg.production('stmt : block')
def statement_block(p):
    return p[0]

@pg.production('stmt : COMMENT')
def statement_comment(p):
    return Comment(p[0].getstr())

@pg.production('optional_comment : COMMENT')
@pg.production('optional_comment : ')
def optional_comment(p):
    if len(p) == 0:
        return None
    return Comment(p[0].getstr())

@pg.production('optional_doccomment : DOCCOMMENT')
@pg.production('optional_doccomment : ')
def optional_comment(p):
    if len(p) == 0:
        return None
    return Comment(p[0].getstr())

@pg.production('optional_attributes : attribute optional_attributes')
@pg.production('optional_attributes : ')
def optional_attributes(p):
    if len(p) == 0:
        return []
    return [ p[0] ] + p[1]

@pg.production('attribute : AT IDENTIFIER OPEN_PARENS expression_list CLOSE_PARENS')
@pg.production('attribute : AT IDENTIFIER')
def attribute(p):
    if len(p) == 2:
        return Attribute(p[1].getstr())
    return Attribute(p[1].getstr(), p[3])

@pg.production('stmt : optional_attributes LET IDENTIFIER type_expr_or_empty initialization_expr SEMICOLON')
def statement_let(p):
    return LetStatement(p[2].getstr(), p[3], p[4], p[0])

@pg.production('stmt : IDENTIFIER EQUALS expression SEMICOLON')
def statement_expr(p):
    return Assignment(p[0].getstr(), p[2])

@pg.production('stmt : RETURN optional_expression SEMICOLON')
def statement_expr(p):
    return ReturnStatement(p[1])

@pg.production('optional_expression : expression')
@pg.production('optional_expression : ')
def optional_expr(p):
    if len(p) == 0:
        return None
    return p[0]

@pg.production('protofunction : FUNCTION')
def fn_qualif(p):
    return Function

@pg.production('protofunction : KERNEL')
def kernel_qualif(p):
    return Kernel

@pg.production('protofunction : QUICKCHECK')
def quickcheck_qualif(p):
    return Quickcheck

@pg.production('assumptions : REQUIRES expression_list')
@pg.production('assumptions : ')
def assumptions(p):
    if len(p) == 0:
        return []
    return p[1]

@pg.production('guarantees : ENSURES expression_list')
@pg.production('guarantees : ')
def guarantees(p):
    if len(p) == 0:
        return []
    return p[1]

@pg.production('stmt : optional_doccomment protofunction IDENTIFIER OPEN_PARENS parameters_list CLOSE_PARENS assumptions guarantees block')
def statement_kernel(p):
    protofunc = p[1](p[2].getstr(), p[4], p[8], p[6], p[7])
    protofunc.doc = p[0]
    return protofunc

@pg.production('parameters_list : optional_doccomment parameter COMMA optional_comment parameters_list')
@pg.production('parameters_list : optional_doccomment parameter optional_comment')
@pg.production('parameters_list : ')
def params_list(p):
    if len(p) == 0:
        return []
    if len(p) == 3 or len(p) == 2: # parameter [optional_comment]
        param = p[1]
        param.doc = p[0]
        return [ param ]
    # parameter COMMA optional_comment parameters_list
    param = p[1]
    param.doc = p[0]
    return [ param ] + p[4]

@pg.production('parameter : optional_attributes param_qualifier IDENTIFIER type_expr_or_empty initialization_expr')
def statement_parameter(p):
    return Parameter(p[2].getstr(), p[3], p[4], p[1], p[0])

@pg.production('param_qualifier : IN')
@pg.production('param_qualifier : OUT')
@pg.production('param_qualifier : STATE')
@pg.production('param_qualifier : ')
def param_qualif(p):
    if len(p) == 0:
        return None
    return p[0].getstr()

@pg.production('type_expr_or_empty : DDOTS type_expression')
@pg.production('type_expr_or_empty : ')
def type_expr_or_empty(p):
    if len(p) == 0:
        return None
    return p[1]

@pg.production('qualified_constructor_type : qualified_constructor_type DOT IDENTIFIER')
@pg.production('qualified_constructor_type : IDENTIFIER')
def qualified_constructor_type(p):
    if len(p) == 1:
        return Identifier(p[0].getstr())
    return GetAttribute(p[2].getstr(), p[0])

@pg.production('constructor_type : qualified_constructor_type')
@pg.production('constructor_type : ')
def constructor_type(p):
    if len(p) == 0:
        return None
    return p[0]

@pg.production('type_expression : constructor_type LT type_expression GT')
def type_constructor_call(p):
    if p[0] is None:
        return Stream(p[2])
    if p[0].__class__ == Identifier:
        return MethodCall(p[0].value, None, [ p[2] ])
    method_name = p[0].attr_name
    receiver = p[0].receiver
    return MethodCall(method_name, receiver, [ p[2] ])

@pg.production('type_expression : constructor_type LT type_expression COMMA expression GT')
def type_buffer(p):
    if p[0].__class__ == Identifier:
        kind = p[0].value
    elif p[0].__class__ == GetAttribute:
        kind = p[0].attr_name # Simplification, but usually buffers are not qualified like this?
    else:
        kind = str(p[0])
        
    if kind in ['buffer', 'circular_buffer', 'round_robin']:
        return BufferType(kind, p[2], p[4])
    return MethodCall(kind, None, [ p[2], p[4] ])

@pg.production('type_expression : FIXED_POINT_TYPE')
def type_fixed_point(p):
    s = p[0].getstr()
    signed = s.startswith('Q')
    if s.startswith('UQ'):
        signed = False
        parts = s[2:].split('.')
    else:
        parts = s[1:].split('.')
    return FixedPointType(signed, int(parts[0]), int(parts[1]))

@pg.production('type_expression : OPEN_SQBRACKET type_expression SEMICOLON optional_expression CLOSE_SQBRACKET')
def type_array_of(p):
    return ArrayOf(p[1], p[3])

@pg.production('type_expression : IDENTIFIER')
def type_expression_identifier(p):
    return Identifier(p[0].getstr())

@pg.production('initialization_expr : EQUALS expression')
@pg.production('initialization_expr : ')
def init_expr(p):
    if len(p) == 0:
        return None
    return p[1]

@pg.production('stmt : IDENTIFIER MUL_ASSIGN expression SEMICOLON')
def statement_expr(p):
    return MulAssignment(p[0].getstr(), p[2])

@pg.production('stmt : IDENTIFIER ADD_ASSIGN expression SEMICOLON')
def statement_expr(p):
    return AddAssignment(p[0].getstr(), p[2])

@pg.production('stmt : IDENTIFIER SUB_ASSIGN expression SEMICOLON')
def statement_expr(p):
    return SubAssignment(p[0].getstr(), p[2])

@pg.production('stmt : expression SEMICOLON')
@pg.production('stmt : expression', precedence='COMMA')
def statement_expr(p):
    return p[0]

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

token_to_constructor = {}
token_to_constructor['PLUS'] = Add
token_to_constructor['MINUS'] = Sub
token_to_constructor['MUL'] = Mul
token_to_constructor['DIV'] = Div
token_to_constructor['LT'] = LessThan
token_to_constructor['LEQ'] = LessEquals
token_to_constructor['GT'] = GreaterThan
token_to_constructor['GEQ'] = GreaterEquals
token_to_constructor['DEQUALS'] = Equality
token_to_constructor['DIFFERENT'] = Different
token_to_constructor['AND'] = And
token_to_constructor['OR'] = Or
token_to_constructor['XOR'] = Xor
token_to_constructor['IMPLY'] = Imply
token_to_constructor['MODULO'] = Modulo
token_to_constructor['PIPE'] = BitwiseOr
token_to_constructor['PIPE_RIGHT'] = LinearConnection
token_to_constructor['AMPERSAND'] = BitwiseAnd
token_to_constructor['BTLEFT'] = BitShiftLeft
token_to_constructor['BTRIGHT'] = BitShiftRight

@pg.production('expression : expression AND expression')
@pg.production('expression : expression OR expression')
@pg.production('expression : expression XOR expression')
@pg.production('expression : expression IMPLY expression')
@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
@pg.production('expression : expression MODULO expression')
@pg.production('expression : expression LT expression')
@pg.production('expression : expression LEQ expression')
@pg.production('expression : expression GT expression')
@pg.production('expression : expression GEQ expression')
@pg.production('expression : expression DEQUALS expression')
@pg.production('expression : expression DIFFERENT expression')
@pg.production('expression : expression PIPE expression')
@pg.production('expression : expression PIPE_RIGHT expression')
@pg.production('expression : expression AMPERSAND expression')
@pg.production('expression : expression BTLEFT expression')
@pg.production('expression : expression BTRIGHT expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    constructor = token_to_constructor.get(p[1].gettokentype(), None)
    if constructor is None:
        raise AssertionError('Oops, this should not be possible!')
    else:
        return constructor(left, right)
    

# Only accept limited expression as the normal way is the pow method
@pg.production('expression : expression POW IDENTIFIER')
@pg.production('expression : expression POW NUMBER')
def expression_power(p):
    receiver = p[0]
    power = p[2].getstr()
    if p[2].gettokentype() == 'NUMBER':
        power = Number(power)
    else:
        power = Identifier(power)
    return MethodCall('pow', receiver, [power])

unary_token_to_constructor = {}
unary_token_to_constructor['NOT'] = Not
unary_token_to_constructor['MINUS'] = UnaryMinus
unary_token_to_constructor['BITNEG'] = BitNegation

@pg.production('expression : MINUS expression')
@pg.production('expression : NOT expression')
@pg.production('expression : BITNEG expression')
def expression_unaryop(p):
    inner = p[1]
    constructor = unary_token_to_constructor.get(p[0].gettokentype(), None)
    if constructor is None:
        raise AssertionError('Oops, this should not be possible!')
    else:
        return constructor(inner)
    
@pg.production('expression : expression PRIME')
def expression_unaryop(p):
    inner = p[0]
    return Prime(inner)

@pg.production('argument : expression')
def argument_pos(p):
    return p[0]

@pg.production('argument : IDENTIFIER DDOTS expression')
def argument_named(p):
    return (p[0].getstr(), p[2])

@pg.production('argument_list : argument')
def argument_list_singleton(p):
    return [ p[0] ]

@pg.production('argument_list : argument_list COMMA argument')
def argument_list_tail(p):
    return p[0] + [ p[2] ]

@pg.production('argument_emptylist : argument_list')
@pg.production('argument_emptylist : ')
def argument_emptylist(p):
    if len(p) == 0:
        return []
    return p[0]

def split_args(args):
    positional = []
    named = []
    for a in args:
        if isinstance(a, tuple):
            named.append(a)
        else:
            positional.append(a)
    return positional, named

@pg.production('expression : expression DOT IDENTIFIER OPEN_PARENS argument_emptylist CLOSE_PARENS')
def expression_methodcall(p):
    pos, named = split_args(p[4])
    return MethodCall(p[2].getstr(), p[0], pos, named)

@pg.production('expression : expression OPEN_PARENS argument_emptylist CLOSE_PARENS')
def expression_functioncall(p):
    pos, named = split_args(p[2])
    if p[0].__class__ == Identifier:
        return MethodCall(p[0].value, None, pos, named)
    elif p[0].__class__ == GetAttribute:
        receiver = p[0].receiver
        method_name = p[0].attr_name
        return MethodCall(method_name, receiver, pos, named)
    return MethodCall(None, p[0], pos, named)

@pg.production('expression : expression DOT IDENTIFIER')
def expression_getattr(p):
    return GetAttribute(p[2].getstr(), p[0])

@pg.production('block : OPEN_BRACKETS optional_stmts_list CLOSE_BRACKETS')
def block(p):
    return Block(p[1])

@pg.production('expression : IF expression block else_condition', precedence='IF')
def expression_conditional(p):
    on_stream = p[0].getstr() == 'where'
    return ConditionalExpression(p[1], p[2], p[3], on_stream=on_stream)

@pg.production('else_condition : ELSE block')
@pg.production('else_condition : ')
def expression_else_condition(p):
    if len(p) == 0:
        return None
    return p[1]

@pg.production('expression : MATCH expression OPEN_BRACKETS match_arms CLOSE_BRACKETS')
def expression_match(p):
    return MatchExpression(p[1], p[3])

@pg.production('match_arms : match_arm match_arms')
@pg.production('match_arms : ')
def match_arms(p):
    if len(p) == 0:
        return []
    return [ p[0] ] + p[1]

@pg.production('match_arm : pattern FAT_ARROW expression COMMA')
def match_arm(p):
    return MatchArm(p[0], p[2])

@pg.production('pattern : expression')
def pattern_expr(p):
    return p[0]

@pg.production('pattern : IDENTIFIER')
def pattern_id(p):
    if p[0].getstr() == '_':
        return Identifier('_')
    return Identifier(p[0].getstr())

parser = pg.build()
