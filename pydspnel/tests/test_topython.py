from pydspnel.prettyprinter import PrettyPrinter
from pydspnel import parse
from pydspnel.to_python import ToPython
pp = PrettyPrinter()

def test_to_python():
    topy = ToPython()

    ast_dspnel = parse("let y = 3;")
    assert topy.unparse(ast_dspnel) == "y = 3"

    ast_dspnel = parse("y = x;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = x"

    ast_dspnel = parse("y = foo.bar;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = foo.bar"

    ast_dspnel = parse("y = foo.bar();")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = foo.bar()"

    ast_dspnel = parse("y = a + b;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = a + b"

    ast_dspnel = parse("y = a / b;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = a / b"

    ast_dspnel = parse("y = a * b;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = a * b"

    ast_dspnel = parse("y = 2j;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = 2j"

    ast_dspnel = parse("y = -2j;")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = -2j"

    ast_dspnel = parse("y = foo.bar(a);")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "y = foo.bar(a)"

    ast_dspnel = parse("y = x * np.exp((-2j) * np.pi * target_freq * np.arange(streams_length) / x_sample_rate);")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == 'y = x * np.exp(-2j * np.pi * target_freq * np.arange(streams_length) / x_sample_rate)'

def test_function_to_python():
    topy = ToPython()

    ast_dspnel = parse("fn foo() { return 10;}")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "def foo():\n    return 10"

    ast_dspnel = parse("fn foo(a: u32, b: c64,) { return (a+b);}")
    tgt_python = topy.unparse(ast_dspnel)
    assert tgt_python == "def foo(a, b):\n    return a + b"