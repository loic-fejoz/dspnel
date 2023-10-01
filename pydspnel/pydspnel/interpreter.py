import cmath
import numpy

class DSPMatrix:
    def __init__(self, value, noconvert=None):
        if noconvert:
            self.value = value
        else:
            self.value = numpy.array(value)

    def __eq__(self, other):
        if other.__class__.__name__ == 'DSPMatrix':
            return numpy.array_equal(self.value, other.value, True)
        else:
            return False

    def __repr__(self) -> str:
        return "DSPMatrix(" + str(self.value) + ")"

    def transpose(self):
        val = self.value
        if val.ndim == 1:
            val = numpy.array(val, ndmin=2)
        return DSPMatrix(val.transpose(), True)
    
    def size(self):
        pass

    def len(self):
        s = self.size()
        assert s.len() == 1
        return s[0]

class DSPnelInterpreter:
    def __init__(self) -> None:
        pass

    def evalExpr(self, expr, env):
        kind = expr.__class__.__name__
        if kind == 'Number':
            val = expr.value
            multiplier = 1
            if val.endswith('j') or val.endswith('i'):
                val = val[:-1]
                multiplier = complex(0, 1)
            try:
                return multiplier * int(val)
            except:
                return multiplier * float(val)
        elif kind == 'Add':
            return self.evalExpr(expr.left, env) + self.evalExpr(expr.right, env)
        elif kind == 'Mul':
            return self.evalExpr(expr.left, env) * self.evalExpr(expr.right, env)
        elif kind == 'Sub':
            return self.evalExpr(expr.left, env) - self.evalExpr(expr.right, env)
        elif kind == 'Div':
            return self.evalExpr(expr.left, env) / self.evalExpr(expr.right, env)
        elif kind == 'Matrix':
            return self.evalMatrix(expr, env)
        elif kind == 'Identifier':
            return env[expr.value]
        elif kind == 'MethodCall':
            receiver = self.evalExpr(expr.receiver, env)
            mthd = getattr(receiver, expr.method_name)
            args = [self.evalExpr(arg, env) for arg in expr.args]
            return mthd(*args)
        else:
            raise Exception('Not yet handled: ' + kind)

    def evalMatrix(self, expr, env):
        res = [self.evalRow(row, env) for row in expr.rows]
        if len(res) == 1:
            res = res[0]
        return DSPMatrix(res)

    def evalRow(self, row, env):
        kind = row.__class__.__name__
        if kind == 'Row':
            res = [self.evalExpr(subexpr, env) for subexpr in row.expr_list]
            return res
        elif kind == 'RowIter':
            res = []
            for k in range(self.evalExpr(row.start, env), self.evalExpr(row.stop, env)):
                env[row.identifier.value] = k
                val = self.evalExpr(row.expr, env)
                if val.__class__.__name__ == 'DSPMatrix':
                    res.append(val.value)
                else:
                    res.append(val)
            return res
        else:
            raise Exception('Not yet handled Row: ' + kind)