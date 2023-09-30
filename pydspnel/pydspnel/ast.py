from rply.token import BaseBox

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

class BinaryOp(BaseBox):
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
    
class MethodCall(BaseBox):
    def __init__(self, method_name, receiver, args):
        super().__init__()
        self.method_name = method_name
        self.receiver = receiver
        self.args = args

    def asLisp(self):
        args = ' '.join([arg.asLisp() for arg  in self.args])
        return "(MethodCall {} {} ({}))".format(self.method_name, self.receiver.asLisp(), args)