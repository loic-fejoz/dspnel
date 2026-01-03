from pydspnel.types import *
class TypingPass:
    def __init__(self) -> None:
        pass

    def evalExpr(self, expr, env):
        if expr is None:
            return None
        if isinstance(expr, list):
            for e in expr:
                self.evalExpr(e, env)
            return None
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
                try:
                    val = multiplier * float(val)
                    expr.dspnel_type = env['float']
                except:
                    val = None
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
            expr.dspnel_type = env.get(expr.value)
        elif kind == 'MethodCall':
            receiver_type = self.evalExpr(expr.receiver, env)
            if receiver_type:
                mthd = getattr(receiver_type, expr.method_name, None)
                if mthd:
                    args_types = [self.evalExpr(arg, env) for arg in expr.args]
                    expr.dspnel_type = mthd(*args_types)
                else:
                    # Generic method or kernel instantiation
                    expr.dspnel_type = receiver_type
            else:
                # Top level call (e.g. kernel instantiation or built-in)
                looked_up = env.get(expr.method_name)
                if isinstance(looked_up, KernelType):
                    expr.dspnel_type = looked_up
                else:
                    expr.dspnel_type = None
        elif kind == 'LinearConnection':
            left_type = self.evalExpr(expr.left, env)
            right_type = self.evalExpr(expr.right, env)
            # Basic validation: both sides should be kernels or flowgraphs
            if left_type and right_type:
                expr.dspnel_type = FlowgraphType([left_type, right_type])
            else:
                expr.dspnel_type = None
        elif kind == 'Block':
            for stmt in expr.stmts:
                self.evalExpr(stmt, env)
            expr.dspnel_type = None
        elif kind == 'LetStatement':
            init_type = self.evalExpr(expr.initialization, env)
            env[expr.variable_name] = init_type
            expr.dspnel_type = init_type
        elif kind == 'Kernel':
            inputs = {}
            outputs = {}
            for param in expr.params:
                param_type = self.evalExpr(param.type_expr, env)
                if param.qualifier == 'in':
                    inputs[param.variable_name] = param_type
                elif param.qualifier == 'out':
                    outputs[param.variable_name] = param_type
            expr.dspnel_type = KernelType(expr.name, inputs, outputs)
            env[expr.name] = expr.dspnel_type
        elif kind == 'Identifier':
            expr.dspnel_type = env.get(expr.value)
        elif kind == 'Stream':
            expr.dspnel_type = StreamType(self.evalExpr(expr.inner, env))
        else:
            # For now, just ignore unknown kinds and keep going if possible
            expr.dspnel_type = None
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