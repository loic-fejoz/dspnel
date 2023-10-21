from pydspnel.ast import *
from pydspnel.prettyprinter import PrettyPrinter
from pydspnel import parse

def test_expr():
    pp = PrettyPrinter()
    ast = parse('3 *b')
    assert pp.as_string(ast) == "3 * b"

    ast = parse('3+b')
    assert pp.as_string(ast) == "3 + b"

    ast = parse('3+4*b')
    assert pp.as_string(ast) == "3 + 4 * b"

    ast = parse('a.b')
    assert pp.as_string(ast) == "a.b"

    ast = parse('a.b()')
    assert pp.as_string(ast) == "a.b()"

    ast = parse('a.b(3, bc)')
    assert pp.as_string(ast) == "a.b(3, bc)"

    ast = parse('a.b.c(3, bc, cd)')
    assert pp.as_string(ast) == "a.b.c(3, bc, cd)"

    ast = parse('(3+4)*b')
    assert pp.as_string(ast) == "(3 + 4) * b"

    ast = parse('((not a) and b)')
    assert pp.as_string(ast) == "not a and b"

    ast = parse('not (a and b)')
    assert pp.as_string(ast) == "not (a and b)"

    ast = parse('(6* 3j).re() == 3')
    assert pp.as_string(ast) == "(6 * 3j).re() == 3"

    ast = parse("y = x * x';")
    assert pp.as_string(ast) == "y = x * x';\n"

    ast = parse('foo()')
    assert pp.as_string(ast) == "foo()"

    ast = parse('a.pow(2)')
    assert pp.as_string(ast) == "a^2"

    ast = parse('a.pow(x)')
    assert pp.as_string(ast) == "a^x"

    ast = parse('(a * b).pow(2)')
    assert pp.as_string(ast) == "(a * b)^2"

    ast = parse('a.pow(2 * x)')
    assert pp.as_string(ast) == "a.pow(2 * x)"

def test_kernel():
    pp = PrettyPrinter()
    ast = [Kernel('AGC', params=[], block=Block([]))]
    assert pp.as_string(ast) == """kernel AGC(
) {
}
"""

    ast = Kernel('AGC', params=[], block=Block([
        Assignment('a', Identifier('b'))
    ]))
    assert pp.as_string(ast) == """\nkernel AGC(
) {
    a = b;
}
"""
    ast = parse('kernel foo1(a: u32,){}')
    assert pp.as_string(ast) == """\nkernel foo1(
    a: u32,
) {
}
"""

    ast = parse('kernel foo2(a: u32, bb: c64,){}')
    assert pp.as_string(ast) == """\nkernel foo2(
     a: u32,
    bb: c64,
) {
}
"""

    ast = parse('kernel foo3(a: u32, bb: c64 = 0.0,){}')
    assert pp.as_string(ast) == """\nkernel foo3(
     a: u32,
    bb: c64 = 0.0,
) {
}
"""
    ast = parse('kernel foo3(a: u32, in bb: c64 = 0.0,){}')
    assert pp.as_string(ast) == """\nkernel foo3(
        a: u32,
    in bb: c64 = 0.0,
) {
}
"""

    ast = parse("""kernel foo2(
    a: u32,
    /// the second parameter                
    bb: c64,){}""")
    assert pp.as_string(ast) == """\nkernel foo2(
    a: u32,
    /// the second parameter
    bb: c64,
) {
}
"""

    ast = parse("""kernel foo2(
    /// the first parameter
     a: u32,
    bb: c64,){}""")
    assert pp.as_string(ast) == """\nkernel foo2(
    /// the first parameter
     a: u32,
    bb: c64,
) {
}
"""

    ast = parse("""kernel foo2(
    /// the first parameter
     a: u32 = 3,
    bb: c64,){}""")
    assert pp.as_string(ast) == """\nkernel foo2(
    /// the first parameter
     a: u32 = 3,
    bb: c64,
) {
}
"""

    ast = parse("""kernel foo2(
    /// the first parameter
     a: u32 = 3,
    bb: freq = 45,){}""")
    assert pp.as_string(ast) == """\nkernel foo2(
    /// the first parameter
     a: u32  = 3,
    bb: freq = 45,
) {
}
"""

    ast = parse("""kernel foo1(x: <c32>, y: <c32>,){
    // apply gain to input sample
    y = 3 * x;
    }""")
    assert pp.as_string(ast) == """\nkernel foo1(
    x: <c32>,
    y: <c32>,
) {
    // apply gain to input sample
    y = 3 * x;
}
"""

    ast = parse("""kernel foo1(x: <c32>, y: <c32>,){
    // apply gain to input sample
    y = 3 * x;
    // not enough
    y = 2 * y;
    }""")
    assert pp.as_string(ast) == """\nkernel foo1(
    x: <c32>,
    y: <c32>,
) {
    // apply gain to input sample
    y = 3 * x;
    
    // not enough
    y = 2 * y;
}
"""

def test_stmt():
    pp = PrettyPrinter()
    ast = parse('a += 3 * b;')
    assert pp.as_string(ast) == "a += 3 * b;\n"

    ast = parse('let a: u32 = 3 * b;')
    assert pp.as_string(ast) == "let a: u32 = 3 * b;\n"

    ast = parse('a += 3 * b;\n b = 3 * a;')
    assert pp.as_string(ast) == "a += 3 * b;\nb = 3 * a;\n"

    ast = parse('a += 3 * b;\na.debug();b = 3 * a;')
    assert pp.as_string(ast) == "a += 3 * b;\na.debug();\nb = 3 * a;\n"

def test_function():
    pp = PrettyPrinter()
    ast = [Function('AGC', params=[], block=Block([]))]
    assert pp.as_string(ast) == """fn AGC(
) {
}
"""

    ast = [Function('foo', params=[], block=Block([])), Function('bar', params=[], block=Block([]))]
    assert pp.as_string(ast) == """fn foo(
) {
}

fn bar(
) {
}
"""

    ast = parse("""
fn cosine(
          sample_rate: samprate,
                 freq: freq,
            amplitude: f64,
               offset: f64   = 0,
        initial_phase: phase = 0,
    out             y: <f64>,
) {
    
}
                """)
    assert pp.as_string(ast) == """
fn cosine(
          sample_rate: samprate,
                 freq: freq,
            amplitude: f64,
               offset: f64      = 0,
        initial_phase: phase    = 0,
    out             y: <f64>,
) {
}
"""

def test_param():
    pp = PrettyPrinter()

    ast = Parameter('a', Identifier('u32'), initialization=Number('3'))
    assert pp.pp_param(ast) == ['', 'a: ', 'u32 ', '= 3,']

    ast = Parameter('bb', Identifier('freq'), initialization=Number('45'))
    assert pp.pp_param(ast) == ['', 'bb: ', 'freq ', '= 45,']

def test_matrix():
    pp = PrettyPrinter()

    ast = parse("[1, 2, 3, 4, 5, 6]")
    assert pp.as_string(ast) == """[1, 2, 3, 4, 5, 6]"""

    ast = parse("a = [1, 2, 3, 4, 5, 6];")
    assert pp.as_string(ast) == """a = [1, 2, 3, 4, 5, 6];\n"""

    ast = parse("[1, 2, 3; 4, 5, 6]")
    assert pp.as_string(ast) == """[1, 2, 3;
 4, 5, 6]"""

    ast = parse("let a = [1, 2, 3; 4, 5, 6];")
    assert pp.as_string(ast) == """let a =
    [1, 2, 3;
     4, 5, 6];
"""

    ast = parse("let a = [1, 2, 3];")
    assert pp.as_string(ast) == """let a = [1, 2, 3];\n"""