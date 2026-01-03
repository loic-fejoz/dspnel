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
                val = multiplier * int(val)
            except:
                val = multiplier * float(val)
            return (val)
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
        elif kind == 'Prime':
            # Prime operator returns the previous value from the history
            # For now, we only support priming identifiers
            if expr.inner.__class__.__name__ == 'Identifier':
                history = env.get('__history__', {})
                return history.get(expr.inner.value, 0) # Default to 0 if no history
            else:
                raise Exception('Prime operator currently only supported on Identifiers')
        elif kind == 'MethodCall':
            receiver = self.evalExpr(expr.receiver, env)
            mthd = getattr(receiver, expr.method_name, None)
            if mthd:
                args = [self.evalExpr(arg, env) for arg in expr.args]
                return mthd(*args)
            else:
                mthd = getattr(expr.receiver.dspnel_type, 'dsp_' + expr.method_name)
                args = [receiver] + [self.evalExpr(arg, env) for arg in expr.args]
                return mthd(*args)
        else:
            raise Exception('Not yet handled: ' + kind)

    def evalStmt(self, stmt, env):
        kind = stmt.__class__.__name__
        if kind == 'Assignment':
            val = self.evalExpr(stmt.expr, env)
            env[stmt.variable_name] = val
        elif kind == 'LetStatement':
            if stmt.initialization:
                val = self.evalExpr(stmt.initialization, env)
            else:
                val = None
            env[stmt.variable_name] = val
        elif kind == 'ReturnStatement':
            return self.evalExpr(stmt.expr, env)
        elif kind == 'Block':
            return self.evalBlock(stmt, env)
        else:
            # Try to evaluate as expression if it's not a known statement
            return self.evalExpr(stmt, env)

    def evalBlock(self, block, env):
        res = None
        for stmt in block.stmts:
            res = self.evalStmt(stmt, env)
        return res

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

class KernelInterpreter:
    def __init__(self, kernel_node, static_args=None) -> None:
        self.kernel = kernel_node
        self.env = {'__history__': {}}
        self.interpreter = DSPnelInterpreter()
        
        if static_args is None:
            static_args = {}

        # Initialize parameters and state
        for param in kernel_node.params:
            if param.qualifier == 'state':
                if param.initialization:
                    val = self.interpreter.evalExpr(param.initialization, {})
                    self.env[param.variable_name] = val
                else:
                    self.env[param.variable_name] = 0
            elif param.qualifier is None: # Static parameter
                if param.variable_name in static_args:
                    self.env[param.variable_name] = static_args[param.variable_name]
                elif param.initialization:
                    val = self.interpreter.evalExpr(param.initialization, {})
                    self.env[param.variable_name] = val

    def step(self, inputs):
        # inputs is a dict mapping input stream names to current values
        # 1. Update history for inputs and potentially internal variables
        # For simplicity, we save the current env to history before update
        for k, v in self.env.items():
            if k != '__history__':
                self.env['__history__'][k] = v
        
        # 2. Update inputs
        for k, v in inputs.items():
            self.env[k] = v
        
        # 3. Execute kernel block
        self.interpreter.evalBlock(self.kernel.block, self.env)
        
        # 4. Collect outputs
        outputs = {}
        for param in self.kernel.params:
            if param.qualifier == 'out':
                outputs[param.variable_name] = self.env.get(param.variable_name)
        
        return outputs