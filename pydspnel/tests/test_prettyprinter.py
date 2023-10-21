from pydspnel.ast import *
from pydspnel.prettyprinter import PrettyPrinter
from pydspnel import parse

def test_epr():
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

def test_kernel():
    pp = PrettyPrinter()
    ast = Kernel('AGC', params=[], block=Block([]))
    assert pp.as_string(ast) == """kernel AGC(
) {
}
"""

    ast = Kernel('AGC', params=[], block=Block([
        Assignment('a', Identifier('b'))
    ]))
    assert pp.as_string(ast) == """kernel AGC(
) {
    a = b;
}
"""
    ast = parse('kernel foo1(a: u32,){}')
    assert pp.as_string(ast) == """kernel foo1(
    a: u32,
) {
}
"""

    ast = parse('kernel foo2(a: u32, bb: c64,){}')
    assert pp.as_string(ast) == """kernel foo2(
     a: u32,
    bb: c64,
) {
}
"""

    ast = parse('kernel foo3(a: u32, bb: c64 = 0.0,){}')
    assert pp.as_string(ast) == """kernel foo3(
     a: u32,
    bb: c64 = 0.0,
) {
}
"""
    ast = parse('kernel foo3(a: u32, in bb: c64 = 0.0,){}')
    assert pp.as_string(ast) == """kernel foo3(
        a: u32,
    in bb: c64 = 0.0,
) {
}
"""

    ast = parse("""kernel foo2(
    a: u32,
    /// the second parameter                
    bb: c64,){}""")
    assert pp.as_string(ast) == """kernel foo2(
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
    assert pp.as_string(ast) == """kernel foo2(
    /// the first parameter
     a: u32,
    bb: c64,
) {
}
"""

    ast = parse("""kernel foo1(x: <c32>, y: <c32>,){
    // apply gain to input sample
    y = 3 * x;
    }""")
    assert pp.as_string(ast) == """kernel foo1(
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
    assert pp.as_string(ast) == """kernel foo1(
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