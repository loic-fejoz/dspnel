import sys
from rply.errors import ParsingError, LexingError
from pydspnel import parseFile
from pydspnel.ast import asLisp
from pydspnel.prettyprinter import PrettyPrinter

def displayError(pos):
    with open(filename) as f:
        lc = 1
        for line in f:
            if lc == pos.lineno - 1:
                sys.stderr.write(line)
            if lc == pos.lineno:
                sys.stderr.write(line)
                for i in range(pos.colno-1):
                    sys.stderr.write('-')
                sys.stderr.write('^\n')
                break
            lc = lc + 1
    sys.stderr.flush()

filename = sys.argv[1]
try:
    ast = parseFile(filename)
    pp = PrettyPrinter()
    print(pp.as_string(ast))
    sys.exit(0)
except ParsingError as pe:
    sys.stderr.write(repr(pe))
    sys.stderr.write('\n')
    displayError(pe.getsourcepos())
    sys.exit(1)
except LexingError as le:
    sys.stderr.write(repr(le))
    sys.stderr.write('\n')
    displayError(le.getsourcepos())
    sys.exit(1)