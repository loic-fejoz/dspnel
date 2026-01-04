from pydspnel.lexer import lexer
from pydspnel.parser import parser
from pydspnel.interpreter import DSPnelInterpreter
from pydspnel.typing_pass import applyTypingPass
from pydspnel.pynumpy_backend import to_python
from pydspnel.diagram_backend import to_mermaid

def parse(src, state=None):
    ast = parser.parse(lexer.lex(src))
    if type(ast) == type([]):
        if len(ast) == 1:
            ast = ast[0]
    return ast

def parseFile(filename):
    with open(filename) as f:
        content = ''.join(f.readlines())
    return parse(content)

def parseAndTypes(src):
    ast = parse(src)
    applyTypingPass(ast)
    return ast

def eval(src, env = None):
    if env is None:
        env = {}
    ast = parseAndTypes(src)
    interpreter = DSPnelInterpreter()
    return interpreter.evalExpr(ast, env)