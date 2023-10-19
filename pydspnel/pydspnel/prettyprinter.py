from pydspnel.ast import *

def nest(depth, doc):
    prefix = ' ' * 4 * depth
    for line in layout(doc):
        yield prefix
        for txt in line:
            yield txt

def concat(docs):
    for doc in docs:
        if type(doc) == type(""):
            yield doc
            continue
        for txt in doc:
            yield txt

def sep(separator, docs):
    prev = None
    for doc in docs:
        if prev is not None:
            yield separator
        if type(doc) == type(""):
            yield doc
            prev = True
            continue
        for txt in doc:
            prev = True
            yield txt

def bracket(prefix, nested, suffix):
    return concat([prefix, nest(1, nested), suffix])

def output(value):
    for v in value:
        print(v, end="")

def doc_len(doc):
    l = 0
    for str in doc:
        l = l + len(str)
    return l

def table(rows, colsfmt, seps=None):
    max_col_width = {}
    for row in rows:
        for j, col in enumerate(row):
            max_col_width[j] = max(max_col_width.get(j, 0), doc_len(col))
    for row in rows:
        for (j, col), fmt in zip(enumerate(row), colsfmt):
            if fmt == 'right':
                yield (max_col_width[j] - doc_len(col)) * ' '
            if type(col) == type(""):
                yield col
            else:
                for str in col:
                    yield str
            if fmt == 'left':
                yield (max_col_width[j] - doc_len(col)) * ' '
            if seps:
                if type(seps) == type(""):
                    yield seps
                else:
                    yield seps[j]
        yield "\n"

def layout(doc):
    acc = ""
    for txt in doc:
        if type(txt) == str:
            acc = acc + txt
            if txt.endswith("\n"):
                yield acc
                acc = ""
        else:
            for line in layout(txt):
                yield line
    if acc != "":
        yield acc
        yield "\n"

def rstrip(doc):
    acc = ""
    for txt in doc:
        if type(txt) == str:
            acc = acc + txt
            if txt.endswith("\n"):
                yield acc.rstrip()
                yield '\n'
                acc = ""
        else:
            for line in rstrip(txt):
                yield line
    if acc != "":
        yield acc.rstrip()
        yield "\n"

class PrettyPrinter:
    def __init__(self) -> None:
        self.binary_ops = {
            And: ' and ',
            Or: ' or ',
            Xor: ' xor ',
            Imply: ' ==> ',
            Add: ' + ',
            Sub: ' - ',
            Mul: ' * ',
            Div: ' / ',
            Modulo: ' % ',
            LessThan: ' < ',
            LessEquals: ' <= ',
            GreaterThan: ' > ',
            GreaterEquals: ' >= ',
            Equality: ' == ',
            Different: ' != ',
            Pipe: ' | ',
            LinearConnection: ' | ',
            BitwiseOr: ' | ',
            BitwiseAnd: ' & ',
            BitShiftLeft: ' << ',
            BitShiftRight: ' >> '}

    def pp(self, ast):
        if ast is None:
            return ''
        t = type(ast)
        if t == Statement:
            return concat([t.variable_name, " = ", self.pp(t.expr), ';\n'])
        elif t == Block:
            return concat([self.pp(stmt) for  stmt in ast.stmts])
        elif t in [Assignment, AddAssignment, MulAssignment, SubAssignment]:
            d = {'': ' = ', 'Mul': ' *= ', 'Add': ' += ', 'Sub': ' -= '}
            op = d[ast.prefix]
            return concat([ast.variable_name, op, self.pp(ast.expr), ';\n'])
        elif t == Identifier:
            return [ast.value]
        elif t == Number:
            return [ast.value]
        elif t == Kernel:
            return concat([
                'kernel ', ast.name, bracket("(\n",
                    self.pp_parameters(ast.params),
                ") "),
                bracket("{\n",
                    self.pp(ast.block),
                "}\n")])
        elif t in self.binary_ops.keys():
            return concat([
                self.pp(ast.left),
                self.binary_ops[t],
                self.pp(ast.right),
            ])
        elif t == GetAttribute:
            return concat([
                self.pp(ast.receiver),
                '.',
                ast.attr_name
            ])
        elif t == MethodCall:
            return concat([
                self.pp(ast.receiver),
                '.',
                ast.method_name,
                '(',
                sep(', ', [self.pp(a) for a in ast.args]),
                ')'
            ])
        else:
            raise BaseException("Unknown type {} '{}'".format(repr(t), asLisp(ast)))

    def as_string(self, ast):
        return ''.join(self.pp(ast))
    
    def pp_parameters(self, params):
        return rstrip(table([self.pp_param(param) for param in params],
            colsfmt=['left', 'right', 'left', 'left'],
            seps=['', '', '', '']))

    def pp_param(self, param):
        row = [param.qualifier,
                param.variable_name,
                ''.join(self.pp(param.type_expr)),
                ''.join(self.pp(param.initialization))]
        if row[0] is None:
            row[0] = ''
        else:
            row[0] += ' '
        if row[2]:
            row[1] += ': '
        if row[3]:
            row[3] = ' = ' + row[3]
        if row[-1] == '':
            if row[-2] == '':
                row[2] += ','
            else:
                row[3] += ','
        else:
            row[-1] += ','
        return row