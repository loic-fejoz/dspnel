from pydspnel import parse, to_python
import numpy as np

def test_generate_simple_kernel():
    src = """
    kernel simplest_iir(in x: <f32>, alpha: f32, out y: <f32>,) {
        y = alpha * x + (1.0 - alpha) * x';
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    # Try to execute it
    namespace = {}
    exec(py_code, namespace)
    
    Kernel_simplest_iir = namespace['Kernel_simplest_iir']
    ki = Kernel_simplest_iir(alpha=0.5)
    
    assert ki.step(1.0) == 0.5
    assert ki.step(1.0) == 1.0

def test_generate_counter():
    src = """
    kernel counter(state c: u32 = 0, out y: <u32>,) {
        c = c + 1;
        y = c;
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    
    Kernel_counter = namespace['Kernel_counter']
    ki = Kernel_counter()
    
    assert ki.step() == 1
    assert ki.step() == 2

def test_generate_with_multiple_outputs():
    src = """
    kernel split(in x: <f32>, out y1: <f32>, out y2: <f32>,) {
        y1 = x;
        y2 = x * 2.0;
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    ki = namespace['Kernel_split']()
    
    res = ki.step(10.0)
    assert res == {'y1': 10.0, 'y2': 20.0}

def test_generate_matrix():
    src = """
    kernel mat_gain(in x: <f32>, out y: <[[f32; 2]; 2]>,) {
        y = x * [1.0, 0.0; 0.0, 1.0];
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    ki = namespace['Kernel_mat_gain']()
    
    res = ki.step(5.0)
    assert isinstance(res, np.ndarray)
    assert np.array_equal(res, np.array([[5.0, 0.0], [0.0, 5.0]]))

def test_generate_conditional():
    src = """
    kernel clipper(in x: <f32>, limit: f32, out y: <f32>,) {
        y = if x > limit { limit } else { if x < -limit { -limit } else { x } };
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    ki = namespace['Kernel_clipper'](limit=1.0)
    
    # ConditionalExpression returns the value of the block
    # but our current backend translates it to ternary.
    # dspnel { x } as a block value is (Add c 2) in test_parser.py
    # So { x } should be translated as x.
    
    assert ki.step(0.5) == 0.5
    assert ki.step(1.5) == 1.0
    assert ki.step(-2.0) == -1.0

def test_generate_pipe():
    src = """
    kernel add1(in x: <f32>, out y: <f32>,) { y = x + 1.0; }
    kernel mul2(in x: <f32>, out y: <f32>,) { y = x * 2.0; }
    let chain = add1() |> mul2();
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    
    assert 'chain' in namespace
    pipe = namespace['chain']
    
    assert pipe.step(5.0) == 12.0
