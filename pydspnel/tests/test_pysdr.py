from pydspnel import parse, to_python, to_mermaid
import numpy as np
import os

def test_pysdr_samples_parsing():
    sample_path = os.path.join(os.path.dirname(__file__), '../../samples/pysdr_samples.dspnel')
    with open(sample_path, 'r') as f:
        src = f.read()
    
    ast = parse(src)
    assert ast is not None
    
    # Verify Python generation
    py_code = to_python(ast)
    assert "class Kernel_costas_loop_bpsk" in py_code
    assert "class Kernel_mm_clock_recovery" in py_code
    assert "class Kernel_lms_tap" in py_code
    
    # Verify Mermaid generation
    mermaid = to_mermaid(ast)
    assert "costas_loop_bpsk" in mermaid
    assert "mm_clock_recovery" in mermaid

def test_costas_loop_execution():
    src = """
    kernel costas(in x: <c32>, out y: <c32>, state phase: f32 = 0.0, alpha: f32 = 0.1) {
        let nco = cos(phase) - 1.0j * sin(phase);
        y = x * nco;
        let error = y.re * y.im;
        phase = phase + alpha * error;
    }
    """
    ast = parse(src)
    py_code = to_python(ast)
    
    namespace = {}
    exec(py_code, namespace)
    ki = namespace['Kernel_costas'](alpha=0.1)
    
    # If we feed it a signal with 0.1 phase offset
    # it should eventually track it.
    # Simple check: it runs.
    res = ki.step(complex(np.cos(0.1), np.sin(0.1)))
    assert isinstance(res, complex)
