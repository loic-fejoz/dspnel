from pydspnel import parse
from pydspnel.interpreter import KernelInterpreter

def test_counter():
    src = """
    kernel counter(state c: u32 = 0, out y: <u32>,) {
        c = c + 1;
        y = c;
    }
    """
    ast = parse(src)
    ki = KernelInterpreter(ast)
    
    assert ki.step({}) == {'y': 1}
    assert ki.step({}) == {'y': 2}
    assert ki.step({}) == {'y': 3}

def test_simplest_iir():
    # This is actually a simple FIR-like filter as defined in README
    src = """
    kernel simplest_iir(in x: <f32>, alpha: f32, out y: <f32>,) {
        y = alpha * x + (1.0 - alpha) * x';
    }
    """
    ast = parse(src)
    ki = KernelInterpreter(ast, static_args={'alpha': 0.5})
    
    # x' defaults to 0 on first step
    # x=1.0, alpha=0.5 -> y = 0.5 * 1.0 + 0.5 * 0 = 0.5
    assert ki.step({'x': 1.0}) == {'y': 0.5}
    
    # x=1.0, alpha=0.5, x'=1.0 -> y = 0.5 * 1.0 + 0.5 * 1.0 = 1.0
    assert ki.step({'x': 1.0}) == {'y': 1.0}
    
    # x=0.0, alpha=0.5, x'=1.0 -> y = 0.5 * 0.0 + 0.5 * 1.0 = 0.5
    assert ki.step({'x': 0.0}) == {'y': 0.5}

def test_actual_iir():
    src = """
    kernel actual_iir(in x: <f32>, alpha: f32, out y: <f32>,) {
        y = alpha * x + (1.0 - alpha) * y';
    }
    """
    ast = parse(src)
    ki = KernelInterpreter(ast, static_args={'alpha': 0.1})
    
    # Step 1: x=1.0, y'=0 -> y = 0.1 * 1.0 + 0.9 * 0 = 0.1
    res = ki.step({'x': 1.0})
    assert abs(res['y'] - 0.1) < 1e-6
    
    # Step 2: x=1.0, y'=0.1 -> y = 0.1 * 1.0 + 0.9 * 0.1 = 0.1 + 0.09 = 0.19
    res = ki.step({'x': 1.0})
    assert abs(res['y'] - 0.19) < 1e-6
