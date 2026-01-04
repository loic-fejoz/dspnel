# AGENTS.md - Antigravity & DSPnel Development

## Project Objective
The goal is to create a high-level, mathematically expressive DSL for Digital Signal Processing (DSP), bridge the gap between textbook notation and hardware-efficient implementation, specifically for Software Defined Radio (SDR) applications.

## Language Features (dspnel)
- **Stateful Kernels**: Native support for `state` variables and the $z^{-1}$ delay operator (`'`).
- **Stream-based Composition**: The `|>` operator for chaining kernels into signal pipelines.
- **Fixed-Point Types**: Native `Q<I>.<F>` and `UQ<I>.<F>` notation (e.g., `Q1.15`).
- **Low-level Abstractions**: Explicit buffer types (`circular_buffer`, `round_robin`) and hardware-aware attributes (`@align`, `@rom`).
- **Pattern Matching**: Rust-inspired `match` expressions with wildcard (`_`) support for clean constellation mapping and logic branching.
- **Verification**: Built-in support for `requires` (assumptions) and `ensures` (guarantees) to facilitate formal verification.

## Technical Stack
- **Lexer/Parser**: Python `rply`.
- **Backend**: Python `numpy`.
- **Visualization**: `mermaid.js`.
- **Testing**: `pytest`.
