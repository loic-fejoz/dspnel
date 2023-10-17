from rply.token import BaseBox

def asLisp(v):
    if type(v) == type([]):
        return ' '.join([asLisp(o) for o in v])
    return v.asLisp()

class Number(BaseBox):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def asLisp(self):
        return str(self.value)
    
class Identifier(BaseBox):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def asLisp(self):
        return str(self.value)
    
class Comment(BaseBox):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def asLisp(self):
        return "(Comment {})".format(repr(self.text))
    
class Expression(BaseBox):
    def __init__(self):
        super().__init__()

class BinaryOp(Expression):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def asLisp(self):
        return '({} {} {})'.format(str(self.__class__.__name__), self.left.asLisp(), self.right.asLisp())

class Add(BinaryOp):
    pass

class Sub(BinaryOp):
    pass

class Mul(BinaryOp):
    pass

class Div(BinaryOp):
    pass

class GreaterThan(BinaryOp):
    pass

class GreaterEquals(BinaryOp):
    pass

class LessThan(BinaryOp):
    pass

class LessEquals(BinaryOp):
    pass

class Equality(BinaryOp):
    pass

class Different(BinaryOp):
    pass

class And(BinaryOp):
    pass

class Or(BinaryOp):
    pass

class Xor(BinaryOp):
    pass

class Imply(BinaryOp):
    pass

class Modulo(BinaryOp):
    pass

class UnaryOp(Expression):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def asLisp(self):
        return '({} {})'.format(str(self.__class__.__name__), self.inner.asLisp())

class UnaryMinus(UnaryOp):
    pass

class Not(UnaryOp):
    pass

class Prime(UnaryOp):
    pass

class Row(BaseBox):
    def __init__(self, expr_list):
        super().__init__()
        if expr_list:
            self.expr_list = expr_list[0]
        else:
            self.expr_list = []

    def asLisp(self):
        return '(Row {})'.format(' '.join([expr.asLisp() for expr in self.expr_list]))

class RowIter(BaseBox):
    def __init__(self, expr, identifier, start, stop):
        super().__init__()
        if expr:
            self.expr = expr[0]
        else:
            self.expr = None
        self.identifier = identifier
        self.start = start
        self.stop = stop

    def asLisp(self):
        return '(RowIter {} {} {} {})'.format(
            self.expr.asLisp(),
            self.identifier.asLisp(),
            self.start.asLisp(),
            self.stop.asLisp())

class Matrix(BaseBox):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def asLisp(self):
        return '(Matrix {})'.format(' '.join([row.asLisp() for row in self.rows]))
    
class MethodCall(Expression):
    def __init__(self, method_name, receiver, args):
        super().__init__()
        self.method_name = method_name
        self.receiver = receiver
        self.args = args

    def asLisp(self):
        args = ' '.join([asLisp(arg) for arg  in self.args])
        receiver = self.receiver and self.receiver.asLisp() or '()'
        return "(MethodCall {} {} ({}))".format(self.method_name, receiver, args)
    
class ConditionalExpression(Expression):
    def __init__(self, condition, then_expr, else_expr=None):
        super().__init__()
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def asLisp(self):
        condition = self.condition.asLisp()
        then_expr = self.then_expr.asLisp()
        else_expr = self.else_expr and self.else_expr.asLisp() or '()'
        return "(Cond {} {} {})".format(condition, then_expr, else_expr)


class GetAttribute(Expression):
    def __init__(self, attr_name, receiver):
        super().__init__()
        self.attr_name = attr_name
        self.receiver = receiver

    def asLisp(self):
        return "(GetAttr {} {})".format(self.attr_name, self.receiver.asLisp())    

class Statement(BaseBox):
    def __init__(self):
        super().__init__()

class LetStatement(Statement):
    def __init__(self, variable_name, type_expr=None, initialization=None):
        super().__init__()
        self.variable_name = variable_name
        self.type_expr = type_expr
        self.initialization = initialization

    def asLisp(self):
        type_expr = self.type_expr and self.type_expr.asLisp() or "()"
        init = self.initialization and self.initialization.asLisp() or "()"
        return "(LetStatement {} {} {})".format(self.variable_name, type_expr, init)
    
class Assignment(Statement):
    def __init__(self, variable_name, expr, prefix=None):
        super().__init__()
        self.variable_name = variable_name
        self.expr = expr
        self.prefix = prefix or ''

    def asLisp(self):
        expr = self.expr.asLisp()
        return "({}Assign {} {})".format(self.prefix, self.variable_name, expr)

class MulAssignment(Assignment):
    def __init__(self, variable_name, expr):
        super().__init__(variable_name, expr, 'Mul')

class AddAssignment(Assignment):
    def __init__(self, variable_name, expr):
        super().__init__(variable_name, expr, 'Add')

class SubAssignment(Assignment):
    def __init__(self, variable_name, expr):
        super().__init__(variable_name, expr, 'Sub')

class Block(BaseBox):
    def __init__(self, stmts):
        super().__init__()
        self.stmts = stmts

    def asLisp(self):
        stmts = ' '.join([stmt.asLisp() for stmt  in self.stmts])
        return "(Block {})".format(stmts)
    
class ProtoFunction(Statement):
    def __init__(self, name, params, block, assumptions=None, guarantees=None):
        self.name = name
        self.params = params
        self.block = block
        self.assumptions = assumptions
        self.guarantees = guarantees

    def asLisp(self):
        params = ' '.join([param.asLisp() for param  in self.params])
        block = self.block.asLisp()
        assumptions = ' '.join([e.asLisp() for e in self.assumptions])
        guarantees = ' '.join([e.asLisp() for e  in self.guarantees])
        return "({} {} ({}) {} ({}) ({}))".format(self.prefix, self.name, params, block, assumptions, guarantees)
    
class Kernel(ProtoFunction):
    prefix = 'Kernel'

class Function(ProtoFunction):
    prefix = 'Fn'

class Quickcheck(ProtoFunction):
    prefix = 'Quickcheck'
  
class Parameter(BaseBox):
    def __init__(self, variable_name, type_expr=None, initialization=None, qualifier=None):
        super().__init__()
        self.variable_name = variable_name
        self.type_expr = type_expr
        self.initialization = initialization
        self.qualifier = qualifier

    def asLisp(self):
        type_expr = self.type_expr and self.type_expr.asLisp() or '()'
        init = self.initialization and self.initialization.asLisp() or "()"
        qualif = self.qualifier or '()'
        return "(Param {} {} {} {})".format(self.variable_name, type_expr, init, qualif)
    
class Stream(BaseBox):
    def __init__(self, inner_type):
        super().__init__()
        self.inner = inner_type

    def asLisp(self):
        return "(Stream {})".format(self.inner.asLisp())  
    
class ReturnStatement(Statement):
    def __init__(self, expr=None):
        super().__init__()
        self.expr = expr

    def asLisp(self):
        expr = self.expr and self.expr.asLisp() or '()'
        return "(Return {})".format(expr)