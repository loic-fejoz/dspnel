import numpy as np
from pydspnel.ast import *

class PyNumpyBackend:
    def __init__(self):
        self.indent_level = 0
        self.math_builtins = ['cos', 'sin', 'tan', 'exp', 'sqrt', 'log', 'log10', 'abs', 'angle']
        self.binary_ops = {
            'Add': '+',
            'Sub': '-',
            'Mul': '*',
            'Div': '/',
            'Modulo': '%',
            'BitwiseOr': '|',
            'BitwiseAnd': '&',
            'BitShiftLeft': '<<',
            'BitShiftRight': '>>',
            'Equality': '==',
            'Different': '!=',
            'LessThan': '<',
            'LessEquals': '<=',
            'GreaterThan': '>',
            'GreaterEquals': '>=',
            'And': 'and',
            'Or': 'or',
        }

    def indent(self):
        return "    " * self.indent_level

    def generate(self, ast):
        if ast is None:
            return ""
        if isinstance(ast, list):
            return "\n".join([self.generate(stmt) for stmt in ast])
        
        kind = ast.__class__.__name__
        if kind == 'Number':
            return ast.value
        elif kind == 'Identifier':
            return ast.value
        elif kind in self.binary_ops:
            return f"({self.generate(ast.left)} {self.binary_ops[kind]} {self.generate(ast.right)})"
        elif kind == 'UnaryMinus':
            return f"-({self.generate(ast.inner)})"
        elif kind == 'Not':
            return f"(not {self.generate(ast.inner)})"
        elif kind == 'Assignment':
            return f"{self.generate(ast.expr)}"
        elif kind == 'LetStatement':
            return f"{self.generate(ast.initialization) if ast.initialization else 'None'}"
        elif kind == 'Block':
            return self.generate(ast.stmts[-1]) if ast.stmts else "None"
        elif kind == 'Kernel':
            return self.generate_kernel(ast)
        elif kind == 'ReturnStatement':
            return f"{self.generate(ast.expr)}"
        elif kind == 'Prime':
            if isinstance(ast.inner, Identifier):
                return f"self._prev_{ast.inner.value}"
            else:
                raise Exception("Complex Prime expressions not yet supported in Python backend")
        elif kind == 'MethodCall':
            args = ", ".join([self.generate(a) for a in ast.args])
            if ast.receiver:
                return f"({self.generate(ast.receiver)}).{ast.method_name}({args})"
            else:
                if ast.method_name in self.math_builtins:
                    return f"np.{ast.method_name}({args})"
                return f"Kernel_{ast.method_name}({args})"
        elif kind == 'GetAttribute':
            attr = ast.attr_name
            if attr == 're': attr = 'real'
            if attr == 'im': attr = 'imag'
            return f"({self.generate(ast.receiver)}).{attr}"
        elif kind == 'LinearConnection':
             return f"Pipe({self.generate(ast.left)}, {self.generate(ast.right)})"
        elif kind == 'Matrix':
            rows = []
            for row in ast.rows:
                elements = [self.generate(e) for e in row.expr_list]
                rows.append("[" + ", ".join(elements) + "]")
            return f"np.array([{', '.join(rows)}])"
        elif kind == 'ConditionalExpression':
            if ast.on_stream:
                return f"np.where({self.generate(ast.condition)}, {self.generate(ast.then_expr)}, {self.generate(ast.else_expr)})"
            else:
                return f"({self.generate(ast.then_expr)} if {self.generate(ast.condition)} else {self.generate(ast.else_expr)})"
        elif kind == 'MatchExpression':
            # As expression, we might need a more complex structure, 
            # but for now let's hope it's used where statements are allowed or use a lambda
            res = [f"(lambda x:"]
            self.indent_level += 1
            res.append(f"{self.indent()}match x:")
            self.indent_level += 1
            for arm in ast.arms:
                pattern = self.generate(arm.pattern)
                if pattern == '_':
                    pattern = '_'
                res.append(f"{self.indent()}case {pattern}: return {self.generate(arm.expr)}")
            self.indent_level -= 2
            res.append(f"{self.indent()})({self.generate(ast.expression)})")
            return "\n".join(res)
        else:
            return f"# UNHANDLED: {kind}"

    def generate_kernel(self, kernel):
        name = kernel.name
        params = []
        state_vars = []
        inputs = []
        outputs = []

        for p in kernel.params:
            if p.qualifier == 'state':
                state_vars.append(p)
            elif p.qualifier == 'in':
                inputs.append(p)
            elif p.qualifier == 'out':
                outputs.append(p)
            else:
                params.append(p)

        lines = [f"{self.indent()}class Kernel_{name}:"]
        self.indent_level += 1
        
        # __init__
        init_params = ["self"] + [p.variable_name + ('=' + self.generate(p.initialization) if p.initialization else '') for p in params]
        lines.append(f"{self.indent()}def __init__({', '.join(init_params)}):")
        self.indent_level += 1
        for p in params:
            lines.append(f"{self.indent()}self.{p.variable_name} = {p.variable_name}")
        for p in state_vars:
            init_val = self.generate(p.initialization) if p.initialization else "0"
            lines.append(f"{self.indent()}self.{p.variable_name} = {init_val}")
        
        primed_vars = self.find_primed_vars(kernel.block)
        for var in primed_vars:
            lines.append(f"{self.indent()}self._prev_{var} = 0")
        
        if len(params) == 0 and len(state_vars) == 0 and len(primed_vars) == 0:
            lines.append(f"{self.indent()}pass")

        self.indent_level -= 1
        lines.append("")

        # step
        input_names = ["self"] + [p.variable_name for p in inputs]
        lines.append(f"{self.indent()}def step({', '.join(input_names)}):")
        self.indent_level += 1
        
        # Initialize outputs
        for p in outputs:
             lines.append(f"{self.indent()}{p.variable_name} = None")

        # Load parameters and state to local variables
        for p in params:
             lines.append(f"{self.indent()}{p.variable_name} = self.{p.variable_name}")
        for p in state_vars:
             lines.append(f"{self.indent()}{p.variable_name} = self.{p.variable_name}")
        
        # Body
        lines.append(self.gen_block_as_stmts(kernel.block))

        # Save state back
        for p in state_vars:
            lines.append(f"{self.indent()}self.{p.variable_name} = {p.variable_name}")
        
        # Update history
        for var in primed_vars:
            lines.append(f"{self.indent()}self._prev_{var} = {var}")

        # Return outputs
        out_names = [p.variable_name for p in outputs]
        if len(out_names) == 1:
            lines.append(f"{self.indent()}return {out_names[0]}")
        elif len(out_names) > 1:
            lines.append(f"{self.indent()}return {{{', '.join([repr(n) + ': ' + n for n in out_names])}}}")
        else:
            lines.append(f"{self.indent()}pass")

        self.indent_level -= 2
        return "\n".join(lines)

    def gen_block_as_stmts(self, block):
        lines = []
        for stmt in block.stmts:
             lines.append(self.generate_stmt(stmt))
        return "\n".join(lines)

    def generate_stmt(self, stmt):
        if stmt is None:
            return ""
        kind = stmt.__class__.__name__
        if kind == 'Assignment':
            return f"{self.indent()}{stmt.variable_name} = {self.generate(stmt.expr)}"
        elif kind == 'LetStatement':
            if stmt.initialization:
                return f"{self.indent()}{stmt.variable_name} = {self.generate(stmt.initialization)}"
            return f"{self.indent()}{stmt.variable_name} = None"
        elif kind == 'ReturnStatement':
            return f"{self.indent()}return {self.generate(stmt.expr)}"
        elif kind == 'ConditionalExpression':
             # generate a full if/else
             res = [f"{self.indent()}if {self.generate(stmt.condition)}:"]
             self.indent_level += 1
             res.append(self.gen_block_as_stmts(stmt.then_expr))
             self.indent_level -= 1
             if stmt.else_expr:
                 res.append(f"{self.indent()}else:")
                 self.indent_level += 1
                 res.append(self.gen_block_as_stmts(stmt.else_expr))
                 self.indent_level -= 1
             return "\n".join(res)
        elif kind == 'Block':
             return self.gen_block_as_stmts(stmt)
        elif kind == 'MatchExpression':
             res = [f"{self.indent()}match {self.generate(stmt.expression)}:"]
             self.indent_level += 1
             for arm in stmt.arms:
                 pattern = self.generate(arm.pattern)
                 if pattern == '_': pattern = '_'
                 res.append(f"{self.indent()}case {pattern}:")
                 self.indent_level += 1
                 res.append(f"{self.indent()}{self.generate(arm.expr)}")
                 self.indent_level -= 1
             self.indent_level -= 1
             return "\n".join(res)
        else:
             return f"{self.indent()}{self.generate(stmt)}"

    def find_primed_vars(self, node):
        primed = set()
        if node is None or isinstance(node, (str, int, float, complex)):
            return primed
        if isinstance(node, Prime):
            if isinstance(node.inner, Identifier):
                primed.add(node.inner.value)
        elif isinstance(node, list):
            for item in node:
                primed.update(self.find_primed_vars(item))
        elif hasattr(node, '__dict__'):
            for v in node.__dict__.values():
                primed.update(self.find_primed_vars(v))
        return primed

PIPE_CODE = """
class Pipe:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def step(self, *args, **kwargs):
        res = self.left.step(*args, **kwargs)
        if res is None:
            return None
        if isinstance(res, dict):
            return self.right.step(**res)
        else:
            return self.right.step(res)
"""

def to_python(ast):
    backend = PyNumpyBackend()
    
    # We might have top-level stmts that need to be generated as stmts
    if isinstance(ast, list):
        code = "\n".join([backend.generate_stmt(s) for s in ast])
    else:
        code = backend.generate_stmt(ast)

    return "import numpy as np\n" + PIPE_CODE + "\n" + code
