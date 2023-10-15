from pydspnel import parse
from pydspnel.ast import asLisp

def test_number():
    p = parse
    ast = p('3')
    ast = ast.asLisp()
    assert ast == '3'

    ast = p('3.2')
    ast = ast.asLisp()
    assert ast == '3.2'

    ast = p('3e-2')
    ast = ast.asLisp()
    assert ast == '3e-2'

    ast = p('3j')
    ast = ast.asLisp()
    assert ast == '3j'

def test_arith():
    p = parse
    ast = p('3 + 2')
    ast = ast.asLisp()
    assert ast == '(Add 3 2)'

    ast = p('3 + 2 * 5')
    ast = ast.asLisp()
    assert ast == '(Add 3 (Mul 2 5))'

    ast = p('3 * 2 + 5')
    ast = ast.asLisp()
    assert ast == '(Add (Mul 3 2) 5)'

    ast = p('3 + 2j')
    ast = ast.asLisp()
    assert ast == '(Add 3 2j)'

def test_matrix():
    p = parse
    ast = p('[2, 3]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2 3))'

    ast = p('[2, 4; 3, 5]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2 4) (Row 3 5))'

    ast = p('[2; 5]')
    ast = ast.asLisp()
    assert ast == '(Matrix (Row 2) (Row 5))'

    ast = p('[2*k for k in 0..10]')
    ast = ast.asLisp()
    assert ast == '(Matrix (RowIter (Mul 2 k) k 0 10))'

    ast = p('[2*k for k in 0..10].conj()')
    ast = ast.asLisp()
    assert ast == '(MethodCall conj (Matrix (RowIter (Mul 2 k) k 0 10)) ())'

def test_expr():
    ast = parse('a.b.foo()')
    ast = ast.asLisp()
    assert ast == '(MethodCall foo (GetAttr b a) ())'

    ast = parse("a'")
    ast = ast.asLisp()
    assert ast == '(Prime a)'

    ast = parse('foo(a, b)')
    ast = ast.asLisp()
    assert ast == '(MethodCall foo () (a b))'

    ast = parse('a.b * b.a')
    ast = ast.asLisp()
    assert ast == '(Mul (GetAttr b a) (GetAttr a b))'

    ast = parse('if a { b } else { c }')
    ast = ast.asLisp()
    assert ast == '(Cond a (Block b) (Block c))'

    ast = parse('a < b')
    ast = ast.asLisp()
    assert ast == '(LessThan a b)'

    ast = parse('a > b')
    ast = ast.asLisp()
    assert ast == '(GreaterThan a b)'

    ast = parse('a and b or c')
    ast = ast.asLisp()
    assert ast == '(Or (And a b) c)'

    ast = parse('a or b and c')
    ast = ast.asLisp()
    assert ast == '(Or a (And b c))'

    ast = parse('a ==> b xor c')
    ast = ast.asLisp()
    assert ast == '(Imply a (Xor b c))'

    ast = parse('not a ==> not b xor c')
    ast = ast.asLisp()
    assert ast == '(Imply (Not a) (Xor (Not b) c))'

    ast = parse('a % 2')
    ast = ast.asLisp()
    assert ast == '(Modulo a 2)'  

def test_statement():
    ast = parse('let a;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a () ())'

    ast = parse('let a: u32;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a u32 ())'

    ast = parse('let a: u32 = 3.0;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a u32 3.0)'

    ast = parse('a = 3 * a;')
    ast = ast.asLisp()
    assert ast == '(Assign a (Mul 3 a))'

    ast = parse('a *= 3 + b;')
    ast = ast.asLisp()
    assert ast == '(MulAssign a (Add 3 b))'

    ast = parse('a += 3 + b;')
    ast = ast.asLisp()
    assert ast == '(AddAssign a (Add 3 b))'

    ast = parse('a -= 3 + b;')
    ast = ast.asLisp()
    assert ast == '(SubAssign a (Add 3 b))'    

    ast = parse('{ a = 2 * b; }')
    ast = ast.asLisp()
    assert ast == '(Block (Assign a (Mul 2 b)))'

    ast = parse("""
    {
        a = 2 * b;
        b = c + 2;
    }
                """)
    ast = ast.asLisp()
    assert ast == '(Block (Assign a (Mul 2 b)) (Assign b (Add c 2)))'

    ast = parse("""
    {
        a = 2 * b;
        c + 2
    }
                """)
    ast = ast.asLisp()
    assert ast == '(Block (Assign a (Mul 2 b)) (Add c 2))'

    ast = parse("""
    {
        let a: u32 = 2 * b;
        c + 2
    }
                """)
    ast = ast.asLisp()
    assert ast == '(Block (LetStatement a u32 (Mul 2 b)) (Add c 2))'

    ast = parse('{}')
    ast = ast.asLisp()
    assert ast == '(Block )'

    ast = parse('kernel A(){}')
    ast = ast.asLisp()
    assert ast == '(Kernel A () (Block ) () ())'

    ast = parse("""kernel A(
                a: u32,
    ){}""")
    ast = ast.asLisp()
    assert ast == '(Kernel A ((Param a u32 () ())) (Block ) () ())'

    ast = parse("""kernel A(
                a: u32,
                b: f64 = 0.0,
                state c: u32 = 0,
                in d: f32,
                out e: i16,
    ){}""")
    ast = ast.asLisp()
    assert ast == '(Kernel A ((Param a u32 () ()) (Param b f64 0.0 ()) (Param c u32 0 state) (Param d f32 () in) (Param e i16 () out)) (Block ) () ())'

    ast = parse("""kernel A(
                in d: <f32>,
                out e: <i16>,
    ){}""")
    ast = ast.asLisp()
    assert ast == '(Kernel A ((Param d (Stream f32) () in) (Param e (Stream i16) () out)) (Block ) () ())'

    ast = parse("""
    fn A(
        a: u32,
    ){
        return a;
    }""")
    ast = ast.asLisp()
    assert ast == '(Fn A ((Param a u32 () ())) (Block (Return a)) () ())'

    ast = parse("""
    fn A(
        a: u32,
    )
    {
        return a;
    }""")
    ast = ast.asLisp()
    assert ast == '(Fn A ((Param a u32 () ())) (Block (Return a)) () ())'

    ast = parse("""
    fn A(
        a: u32,
    )
    requires
        a > 10
    {
        return a;
    }""")
    ast = ast.asLisp()
    assert ast == '(Fn A ((Param a u32 () ())) (Block (Return a)) ((GreaterThan a 10)) ())'

    ast = parse("""
    fn A(
        a: u32,
    )
    requires
        a > 10,
        a <= 20
    {
        return a;
    }""")
    ast = ast.asLisp()
    assert ast == '(Fn A ((Param a u32 () ())) (Block (Return a)) ((GreaterThan a 10) (LessEquals a 20)) ())'  


def test_typeexpr():
    ast = parse('let a: u32;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a u32 ())'

    ast = parse('let a: <u32>;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a (Stream u32) ())'

    ast = parse('let a: Option<u32>;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a (MethodCall Option () (u32)) ())'

    ast = parse('let a: foo.bar<u32>;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a (MethodCall bar foo (u32)) ())'

    ast = parse('let a: foo.bar.baz<u32>;')
    ast = ast.asLisp()
    assert ast == '(LetStatement a (MethodCall baz (GetAttr bar foo) (u32)) ())'

def test_comment():
    ast = parse('let a = 3; // todo')
    ast = asLisp(ast)
    assert ast == "(LetStatement a () 3) (Comment '// todo')"

    ast = parse("""
    // todo
    let a = 3;
    """)
    ast = asLisp(ast)
    assert ast == "(Comment '// todo') (LetStatement a () 3)"

    ast = parse('let a = 3; /* todo */')
    ast = asLisp(ast)
    assert ast == "(LetStatement a () 3) (Comment '/* todo */')"

    ast = parse("""
    /* todo */
    let a = 3;
    """)
    ast = asLisp(ast)
    assert ast == "(Comment '/* todo */') (LetStatement a () 3)"

    ast = parse("""kernel A(
                a: u32, // some comments
    ){}""")
    ast = ast.asLisp()
    assert ast == '(Kernel A ((Param a u32 () ())) (Block ) () ())'

    ast = parse("""kernel A(
                /// some doc comments
                a: u32, // some comments
    ){}""")
    lsp = ast.asLisp()
    assert lsp == '(Kernel A ((Param a u32 () ())) (Block ) () ())'
    assert ast.params[0].doc.asLisp() == "(Comment '/// some doc comments')"

    ast = parse("""
    /// kernel's doc
    kernel A(
                /// some doc comments
                a: u32, // some comments
    ){}""")
    lsp = ast.asLisp()
    assert lsp == '(Kernel A ((Param a u32 () ())) (Block ) () ())'
    assert ast.doc.asLisp() == '(Comment "/// kernel\'s doc")'
    assert ast.params[0].doc.asLisp() == "(Comment '/// some doc comments')"