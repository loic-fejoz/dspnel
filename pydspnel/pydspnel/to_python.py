from pydspnel.ast import *
from pydspnel.transformer import AstTransformer
import ast

class ToPython(AstTransformer):
    def visit_Identifier(self, tree):
        return ast.Name(tree.value, ast.Load)
    
    def visit_Number(self, tree):
        return ast.Constant(eval(tree.value))

    def visit_Assignment(self, tree):
        tree = self.generic_visit(tree)
        return ast.Assign([ast.Name(tree.variable_name, ast.Store())], tree.expr)
    
    def visit_LetStatement(self, tree):
        tree = self.generic_visit(tree)
        return ast.Assign([ast.Name(tree.variable_name, ast.Store())], tree.initialization)
    
    def visit_GetAttribute(self, tree):
        receiver = self.visit(tree.receiver)
        return ast.Attribute(value=receiver, attr=tree.attr_name)
    
    def visit_MethodCall(self, tree):
        receiver = self.visit(tree.receiver)
        args = [self.visit(arg) for arg in (tree.args or [])]
        # named_args = self.visit(tree.named_args)
        return ast.Call(ast.Attribute(value=receiver, attr=tree.method_name), args=args, keywords=[])

    def visit_Mul(self, tree):
        tree = self.generic_visit(tree)
        return ast.BinOp(tree.left, ast.Mult(), tree.right)
    
    def visit_Add(self, tree):
        tree = self.generic_visit(tree)
        return ast.BinOp(tree.left, ast.Add(), tree.right)
    
    def visit_Div(self, tree):
        tree = self.generic_visit(tree)
        return ast.BinOp(tree.left, ast.Div(), tree.right)
    
    def visit_UnaryMinus(self, tree):
        tree = self.generic_visit(tree)
        return ast.UnaryOp(operand=tree.inner, op=ast.USub())

    def unparse(self, tree):
        ast_python = self.visit(tree)
        ast.fix_missing_locations(ast_python)
        return ast.unparse(ast_python)