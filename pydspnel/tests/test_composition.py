from pydspnel import parse, eval
from pydspnel.interpreter import KernelInterpreter, CompositeInterpreter

def test_kernel_instantiation():
    src = """
    kernel gain(k: f32, in x: <f32>, out y: <f32>,) {
        y = x * k;
    }
    let g = gain(2.0);
    """
    # We use a custom env so we can inspect it
    env = {}
    eval(src, env)
    
    assert 'gain' in env
    assert 'g' in env
    assert isinstance(env['g'], KernelInterpreter)
    assert env['g'].env['k'] == 2.0

def test_simple_composition():
    src = """
    kernel add1(in x: <f32>, out y: <f32>,) {
        y = x + 1.0;
    }
    kernel mul2(in x: <f32>, out y: <f32>,) {
        y = x * 2.0;
    }
    let pipe = add1() |> mul2();
    """
    env = {}
    eval(src, env)
    
    pipe = env['pipe']
    assert isinstance(pipe, CompositeInterpreter)
    
    # (5 + 1) * 2 = 12
    assert pipe.step({'x': 5.0}) == {'y': 12.0}
    # (0 + 1) * 2 = 2
    assert pipe.step({'x': 0.0}) == {'y': 2.0}

def test_composition_with_state():
    src = """
    kernel counter(state c: u32 = 0, out y: <u32>,) {
        c = c + 1;
        y = c;
    }
    kernel doubler(in x: <u32>, out y: <u32>,) {
        y = x * 2;
    }
    let chained = counter() |> doubler();
    """
    env = {}
    eval(src, env)
    
    chained = env['chained']
    # Step 1: counter -> 1, doubler -> 2
    assert chained.step({}) == {'y': 2}
    # Step 2: counter -> 2, doubler -> 4
    assert chained.step({}) == {'y': 4}

def test_long_chain():
    src = """
    kernel inc(in x: <f32>, out y: <f32>,) { y = x + 1.0; }
    let chain = inc() |> inc() |> inc();
    """
    env = {}
    eval(src, env)
    chain = env['chain']
    # 0 + 1 + 1 + 1 = 3
    assert chain.step({'x': 0.0}) == {'y': 3.0}
