from pydspnel.ast import *

class MermaidBackend:
    def __init__(self):
        self.node_count = 0
        self.nodes = {} # node_id -> label
        self.edges = [] # (sub1, sub2, label)

    def generate(self, ast):
        self.edges = []
        if isinstance(ast, list):
            for stmt in ast:
                self.visit(stmt)
        else:
            self.visit(ast)
        
        lines = ["graph LR"]
        for edge in self.edges:
            src, dst, label = edge
            if label:
                lines.append(f"    {src} -- \"{label}\" --> {dst}")
            else:
                lines.append(f"    {src} --> {dst}")
        return "\n".join(lines)

    def visit(self, node):
        if node is None:
            return None
        
        kind = node.__class__.__name__
        if kind == 'Kernel':
            return self.visit_kernel(node)
        elif kind == 'LinearConnection':
            left = self.visit(node.left)
            right = self.visit(node.right)
            if left and right:
                self.edges.append((left, right, ""))
            return right
        elif kind == 'MethodCall':
            # Instance of a kernel
            node_id = f"node_{id(node)}"
            label = f"{node.method_name}"
            # We could add params to label
            return f"{node_id}([{label}])"
        elif kind == 'Assignment':
            return self.visit(node.expr)
        elif kind == 'LetStatement':
            return self.visit(node.initialization)
        elif kind == 'Block':
            # For a block, maybe just focus on connections inside?
            # But blocks in dspnel usually contain stmts.
            res = None
            for stmt in node.stmts:
                res = self.visit(stmt)
            return res
        return None

    def visit_kernel(self, kernel):
        kernel_id = f"kernel_{kernel.name}"
        inputs = [p for p in kernel.params if p.qualifier == 'in']
        outputs = [p for p in kernel.params if p.qualifier == 'out']
        
        for p in inputs:
            port_id = f"in_{kernel.name}_{p.variable_name}"
            self.edges.append((f"{port_id}[{p.variable_name}]", f"{kernel_id}(({kernel.name}))", ""))
        
        for p in outputs:
            port_id = f"out_{kernel.name}_{p.variable_name}"
            self.edges.append((f"{kernel_id}(({kernel.name}))", f"{port_id}[{p.variable_name}]", ""))
        
        return f"{kernel_id}(({kernel.name}))"

def to_mermaid(ast):
    backend = MermaidBackend()
    return backend.generate(ast)
