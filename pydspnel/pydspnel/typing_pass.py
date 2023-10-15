from pydspnel.types import *
class TypingPass:
    def __init__(self) -> None:
        pass

    def evalExpr(self, expr, env):
        kind = expr.__class__.__name__
        if kind == 'Number':
            expr.dspnel_type = env['integer']
            val = expr.value
            multiplier = 1
            if val.endswith('j') or val.endswith('i'):
                val = val[:-1]
                multiplier = complex(0, 1)
                expr.dspnel_type = env['complex']
            try:
                val = multiplier * int(val)
            except:
                val = multiplier * float(val)
                expr.dspnel_type = env['float']
            expr.constant_value = val
        elif kind == 'Add':
            expr.dspnel_type = self.evalExpr(expr.left, env).add(self.evalExpr(expr.right, env))
        elif kind == 'Mul':
            expr.dspnel_type = self.evalExpr(expr.left, env).mul(self.evalExpr(expr.right, env))
        elif kind == 'Sub':
            expr.dspnel_type = self.evalExpr(expr.left, env).minus(self.evalExpr(expr.right, env))
        elif kind == 'Div':
            expr.dspnel_type = self.evalExpr(expr.left, env).div(self.evalExpr(expr.right, env))
        elif kind == 'Matrix':
            expr.dspnel_type = self.evalMatrix(expr, env)
        elif kind == 'Identifier':
            expr.dspnel_type = env[expr.value]
        elif kind == 'MethodCall':
            receiver = self.evalExpr(expr.receiver, env)
            mthd = getattr(receiver, expr.method_name)
            args = [self.evalExpr(arg, env) for arg in expr.args]
            return mthd(*args)
        else:
            raise Exception('Not yet handled: ' + kind)
        return expr.dspnel_type

    def evalMatrix(self, expr, env):
        return env['matrix']

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
        
def applyTypingPass(ast):
    the_pass = TypingPass()
    the_pass.evalExpr(ast, types_env)
    return the_pass