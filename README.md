# dspnel
A digital signal processing (DSP) programming language and tools to generate kernels in various target language.

## Introduction

Because I am learning and experimenting with Software Defined Radio (SDR), I was lacking a domain-specific language (DSL) to easily experiment some ideas. Moreover because I am using several programming languages (esp. Rust, C++, Python), I do not want to repeat myself.

The goal is thus to have a DSL to:
* express actual graphs and kernels,
* visualize graphs as one may found them in text book,
* apply some transformations and optimizations on graphs,
* generate code in targetted languages.

## Brainstorming

See also files in [samples folder](/samples/).

```dspnel
let a_vector = [2.0, 1.0];
let another_vector = [2.0;
                      1.0];
let a_matrix = [1.0, 2.0;
                3.0, 4.0];
let a_float32: f32 = 1.2;
```

```dspnel
kernel simplest_iir_low_pass_filter(
    in x:  <f32>,
    alpha: f32,
    out y: <f32>) {

    y = alpha * x + (1-alpha) * x';
}
```

```dspnel
kernel to_qpsk(
    in  symbols: <u2>,
    out iq:      <c32>) {
    
    let in_degrees = symbols * 360.0 / 4.0 + 45;
    let in_radians = in_degrees * pi / 180.0;
    iq = in_radians.cos() + 1j * in_radians.sin();
}
```

```dspnel
let k2 = to_qpsk() | simplest_iir_low_pass_filter(0.5);
let k2 = to_qpsk() ! simplest_iir_low_pass_filter(0.5);
let k2 = to_qpsk() : simplest_iir_low_pass_filter(0.5);
kernel k2 {
    let block1 = to_qpsk();
    let block2 = simplest_iir_low_pass_filter(0.5);
    block2.iq -> block1.x;
    // block2 -> block1
    // block1 <- block2
}
```


## Sources of inspiration

* http://www.spiral.net/
* https://faust.grame.fr/
* https://www.gnuradio.org/
* https://www.futuresdr.org/
* https://pysdr.org/
* https://www.khronos.org/openvx/
* https://www.khronos.org/opencl/
* https://gstreamer.freedesktop.org/documentation/tools/gst-launch.html?gi-language=c
* https://alastairreid.github.io/papers/SDR_06/ SPEX: A programming language for software defined radio 
