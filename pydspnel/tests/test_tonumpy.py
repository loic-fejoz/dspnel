from pydspnel.prettyprinter import PrettyPrinter
from pydspnel import parse
from pydspnel.to_numpy import ToNumpy
pp = PrettyPrinter()

def test_to_numpy():
    tnpy = ToNumpy()

    ast = parse("y = x * a.exp();")
    ast_o = tnpy.visit(ast)
    assert pp.as_string(ast_o) == 'y = x * np.exp(a);\n'

    ast = parse("y = x * (-2j * pi * target_freq * streams.range() / x.sample_rate).exp();")
    ast_o = tnpy.visit(ast)
    assert pp.as_string(ast_o) == 'y = x * np.exp(-2j * np.pi * target_freq * np.arange(streams_length) / x_sample_rate);\n'
