from pydspnel.lexer import lexer
from pydspnel.parser import parser
from pydspnel.interpreter import DSPnelInterpreter

def parse(src):
    return parser.parse(lexer.lex(src))

def eval(src, env = None):
    if not env:
        env = {}
    ast = parse(src)
    interpreter = DSPnelInterpreter()
    return interpreter.evalExpr(ast, env)