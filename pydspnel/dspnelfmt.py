import sys
from rply.errors import ParsingError, LexingError
from pydspnel import parseFile
from pydspnel.ast import asLisp
from pydspnel.prettyprinter import PrettyPrinter, output, layout

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument("--check", action="store_true", help="Run in 'check'mode. Exists with 0 if formatted correctly. Exits with 1 and prints a diff if formatting is required")
parser.add_argument("-w", "-o", "--output", help="write result to (source) file instead of stdout", type=argparse.FileType('w'))
parser.add_argument("--color", action="store_true", help='color output')
args = parser.parse_args()

filename = args.file

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

try:
    ast = parseFile(filename)
    pp = PrettyPrinter()
    if args.check:
        with open(filename) as f:
            line_counter = 1
            for (line_input, line_output) in zip(f, layout(pp.pp(ast))):
                if line_input != line_output:
                    print("{}:".format(line_counter))
                    print("<", line_input, end='')
                    print("---")
                    print(">", line_output, end='')
                    sys.exit(1)
                line_counter += 1
    else:
        output(pp.pp(ast))
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