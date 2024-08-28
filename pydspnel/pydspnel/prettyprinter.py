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

def table(rows, colsfmt, seps=None, last_nl=True, end=None):
    max_col_width = {}
    last_index = len(rows) - 1
    for row in rows:
        for j, col in enumerate(row):
            max_col_width[j] = max(max_col_width.get(j, 0), doc_len(col))
    for i, row in enumerate(rows):
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
        if i != last_index | last_nl:
            yield '\n'
        if i == last_index and end and last_nl:
            yield end

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

def skip(nb, doc):
    i = 1
    for txt in doc:
        if i > nb:
            yield txt
        i += 1

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
        
        self.binary_priority = {
            Not: 6,
            And: 5,
            Or: 4,
            Xor: 4,
            Imply: 3,
            Add: 11,
            Sub: 11,
            Mul: 12,
            Div: 12,
            Modulo: 12,
            LessThan: 7,
            LessEquals: 7,
            GreaterThan: 7,
            GreaterEquals: 7,
            Equality: 7,
            Different: 7,
            Pipe: 8,
            LinearConnection: 8,
            BitwiseOr: 8,
            BitwiseAnd: 9,
            BitShiftLeft: 10,
            BitShiftRight: 10,
            BitNegation: 13,
            Prime: 15,
            GetAttribute: 16,
            MethodCall: 16,
            Identifier: 100,
            Number: 100,
            }

    def pp(self, ast):
        if ast is None:
            return ''
        t = type(ast)
        if t == Statement:
            return concat([t.variable_name, " = ", self.pp(t.expr), ';\n'])
        elif t == Block:
            return self.pp_list(ast.stmts)
        elif t in [Assignment, AddAssignment, MulAssignment, SubAssignment]:
            d = {'': ' = ', 'Mul': ' *= ', 'Add': ' += ', 'Sub': ' -= '}
            op = d[ast.prefix]
            return concat([ast.variable_name, op, self.pp(ast.expr), ';\n'])
        elif t == Identifier:
            return [ast.value]
        elif t == Number:
            return [ast.value]
        elif t in [Kernel, Function, Quickcheck]:
            d = {Kernel: 'kernel ', Function: 'fn ', Quickcheck: 'quickcheck '}
            if ast.assumptions or ast.guarantees:
                end_param = concat([')', '\n'])
            else:
                end_param = ') '
            if ast.assumptions:
                assumptions = concat(['requires', '\n', nest(1, self.pp_bool_expr(ast.assumptions))])
            else:
                assumptions = ''
            if ast.guarantees:
                guarantees = concat(['ensures', '\n', nest(1, self.pp_bool_expr(ast.guarantees))])
            else:
                guarantees = ''
            return concat(['\n',
                d[t], ast.name, bracket("(\n",
                    self.pp_parameters(ast.params),
                end_param),
                assumptions,
                guarantees,
                bracket("{\n",
                    self.pp(ast.block),
                "}\n")])
        elif t in self.binary_ops.keys():
            current_priority = self.priority(ast)
            return concat([
                self.maybe_paren(current_priority, ast.left),
                self.binary_ops[t],
                self.maybe_paren(current_priority, ast.right),
            ])
        elif t == GetAttribute:
            return concat([
                self.maybe_paren(self.priority(ast), ast.receiver),
                (not ast.is_meta and '.') or '@',
                ast.attr_name
            ])
        elif t == MethodCall:
            if ast.receiver is None:
                receiver_chunk = []
            else:
                receiver_chunk = [
                    self.maybe_paren(self.priority(ast), ast.receiver),
                    '.']
            if ast.method_name == 'pow':
                if len(ast.args) == 1 and type(ast.args[0]) in [Identifier, Number]:
                    return concat(receiver_chunk[:-1] + [
                '^',
                self.pp(ast.args[0])
            ])
            return concat(receiver_chunk + [
                ast.method_name,
                '(',
                sep(', ', [self.pp(a) for a in ast.args]),
                ')'
            ])
        elif t == Stream:
            return concat(['<', self.pp(ast.inner), '>'])
        elif t == Comment:
            return concat(['\n', ast.text, '\n'])
        elif t == LetStatement:
            return self.pp_letstmt(ast)
        elif t == Prime:
            return concat([self.maybe_paren(self.priority(ast), ast.inner), "'"])
        elif t == UnaryMinus:
            return concat(['-', self.pp(ast.inner)])
        elif t == Not:
            current_prio = self.priority(ast)
            return concat(['not ', self.maybe_paren(current_prio, ast.inner)])
        elif t == ConditionalExpression:
            return concat(['if ', self.pp(ast.condition), ' ', bracket('{\n', self.pp(ast.then_expr), '}\n')])
        elif t == ReturnStatement:
            if ast.expr:
                return concat(['return ', self.pp(ast.expr), ';\n'])
            else:
                return 'return;\n'
        elif t == list:
            return self.pp_list(ast)
        elif t == Matrix:
            return self.pp_matrix(ast, last_nl=False)
        elif t == ArrayOf:
            return self.pp_arrayof(ast)
        else:
            raise BaseException("Unknown type {} '{}'".format(repr(t), asLisp(ast)))
        
    def pp_list(self, stmts):
        pp_stmts = []
        for stmt in stmts:
            pp = self.pp(stmt)
            if isinstance(stmt, Statement) or isinstance(stmt, Comment) or isinstance(stmt, ConditionalExpression):
                pp_stmts.append(pp)
            else:
                pp_stmts.append(concat([pp, ';', '\n']))
        result = concat(pp_stmts)
        if len(stmts) > 0 and type(stmts[0]) in [Comment, Kernel, Function]:
            result = skip(1, result)
        return result

    def pp_bool_expr(self, stmts):
        pp_stmts = []
        for stmt in stmts:
            pp = self.pp(stmt)
            pp_stmts.extend([pp, ',', '\n'])
        pp_stmts = pp_stmts[:-2]
        pp_stmts.append('\n')
        result = concat(pp_stmts)
        return result

    def maybe_paren(self, outer_priority, ast):
        current_priority = self.priority(ast)
        if current_priority < outer_priority:
            return concat(["(", self.pp(ast), ")"])
        else:
            return self.pp(ast)
    
    def priority(self, ast):
        ast_type = type(ast)
        return self.binary_priority.get(ast_type, 0)

    def pp_letstmt(self, ast):
        is_multineline_matrix = type(ast.initialization) == Matrix and len(ast.initialization.rows) > 1
        if is_multineline_matrix:
            pp_init = ''
            semicolon = ''
        else:
            pp_init = self.pp(ast.initialization)
            pp_init = ''.join(pp_init)
            semicolon = ';'
        row = [ 'let ',
                ast.variable_name,
                ''.join(self.pp(ast.type_expr)),
                pp_init]
        if row[2]:
            row[1] += ': '
        if row[3]:
            row[3] = ' = ' + row[3]
        if is_multineline_matrix:
            row[3] = ' ='
        if row[-1] == '':
            if row[-2] == '':
                row[2] += semicolon
            else:
                row[3] += semicolon
        else:
            row[-1] += semicolon
        if is_multineline_matrix:
            pp_init = self.pp_matrix(ast.initialization, end=';\n')
            return concat(row + ['\n', nest(1, pp_init)])
        else:
            return concat(row + ['\n'])

    def as_string(self, ast):
        return ''.join(self.pp(ast))
    
    def pp_parameters(self, params):
        output = ''
        params_sequences = []
        for param in params:
            if param.doc:
                if len(params_sequences) != 0:
                    output = concat([
                        output,
                        rstrip(table(params_sequences,
                            colsfmt=['left', 'right', 'left', 'left'],
                            seps=['', '', '', ''])),
                        param.doc.text.rstrip(),
                        "\n",
                    ])
                    params_sequences = []
                else:
                    output = concat([output, param.doc.text.rstrip(), '\n'])
            params_sequences.append(self.pp_param(param))
        if len(params_sequences) != 0:
            output = concat([
                        output,
                        rstrip(table(params_sequences,
                            colsfmt=['left', 'right', 'left', 'left'],
                            seps=['', '', '', '']))
                    ])
        return output

    def pp_param(self, param):
        row = [
            param.qualifier,
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
            row[2] += ' '
            row[3] = '= ' + row[3]
        if row[3].rstrip() == '':
            if row[2].rstrip() == '':
                row[1] = row[1].rstrip() + ','
            else:
                row[2] = row[2].rstrip() + ','
        else:
            row[3] = row[3].rstrip() + ','
        return row
    
    def pp_matrix(self, ast, last_nl=True, end='\n'):
        use_iterable = any(map(lambda x: isinstance(x, RowIter), ast.rows))
        if use_iterable:
            raise BaseException("TODO")
        content = []
        width = 0
        for row in ast.rows:
            line_content = ['']
            for expr in row.expr_list:
                line_content.append(self.as_string(expr))
            line_content.append(';')
            content.append(line_content)
            width = max(width, len(line_content))
        colsfmt = ['right'] * width
        seps = [''] + [', '] * (width-3) + ['', '']
        content[0][0] = '['
        content[-1][-1] = ']'
        return table(content, colsfmt, seps, last_nl=last_nl, end=end)
    
    def pp_arrayof(self, ast):
        if ast.size == None:
            return concat(['[', self.pp(ast.inner), ';]'])
        return concat(['[', self.pp(ast.inner), ';', self.pp(ast.size), ']'])