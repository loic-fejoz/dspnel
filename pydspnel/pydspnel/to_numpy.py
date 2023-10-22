from pydspnel.ast import *
from pydspnel.transformer import AstTransformer

class ToNumpy(AstTransformer):
    def visit_MethodCall(self, ast):
        ast = self.generic_visit(ast)
        if ast.method_name == 'exp':
            return MethodCall('exp', Identifier('np'), [ast.receiver])
        elif ast.method_name == 'range' and type(ast.receiver) == Identifier and ast.receiver.value == 'streams':
            return MethodCall('arange', Identifier('np'), [Identifier('streams_length')])
        return ast
    
    def visit_GetAttribute(self, ast):
        if ast.attr_name == 'sample_rate' and type(ast.receiver) == Identifier:
            return Identifier(ast.receiver.value + '_sample_rate')
        return ast
    
    def visit_Identifier(self, ast):
        if ast.value == 'pi':
            return GetAttribute('pi', Identifier('np'))
        return ast
