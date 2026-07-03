# README

## Final Answer

| Variable | Value |
|---|---|
| θ | **30°** (0.5236 rad) |
| M | **0.03** |
| X | **55** |

**Desmos / LaTeX submission string:**
```latex
\left(t*\cos(0.5236)-e^{0.03\left|t\right|}\cdot\sin(0.3t)\sin(0.5236)+55,42+t*\sin(0.5236)+e^{0.03\left|t\right|}\cdot\sin(0.3t)\cos(0.5236)\right)
```
Domain: `6 ≤ t ≤ 60`

## Repo Structure

This repo documents our journey to finding the exact parameters. It includes both our initial flawed approach and the final successful global optimization strategy. Each approach is in its own folder with runnable code and a dedicated README:

```
xy_data.csv                        <- Original data
AlgebraicDecoupling/               <- WRONG: Approach 1 using PCA and algebraic decoupling (biased)
Globaloptim/                       <- CORRECT: Approach 2 using direct global optimization (Differential Evolution)
```

Each folder contains a `README.md` that explains the methodology, the actual output, and the conclusions drawn from that step.

## The Journey, Summarized

| # | Approach | Result | Why it failed / what we learned |
|---|---|---|---|
| 1 | **Algebraic Decoupling** (PCA-based) | L1 Error = ~3.8 | The non-linear coupling meant proxy objectives introduced bias at every stage. We learned that staged decoupling propagates error. |
| 2 | **Direct Global Optimization** | L1 Error = 0.0305 | Correct! By jointly estimating all three parameters against the Chamfer-L1 distance using Differential Evolution, we avoided local minima and staging biases. Recovered true parameters: θ=30°, M=0.03, X=55. |

## How to Reproduce

```bash
pip install numpy pandas scipy

# Run Approach 1 (Algebraic Decoupling)
cd AlgebraicDecoupling
python3 algebraic_decoupling.py
cd ..

# Run Approach 2 (Global Optimization)
cd Globaloptim
python3 globaloptim.py
cd ..
```
