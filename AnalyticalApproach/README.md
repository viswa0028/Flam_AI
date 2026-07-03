# Analytical Approach

## Idea

Since the curve was confirmed **non-self-intersecting** over `t ∈ (6,60)`
(checked in GlobalOptim), its two arc-length **endpoints in the data must
correspond to `t=6` and `t=60`, the two most extreme points along the
curve's principal direction. Once we identify those two points, we get 4
equations (`x,y` at each) in only 3 unknowns (`θ, M, X`):

```
x(6)  = 6*cos(θ)  - g(6)*sin(θ)  + X       g(t) = e^(M|t|)·sin(0.3t)
y(6)  = 42 + 6*sin(θ)  + g(6)*cos(θ)
x(60) = 60*cos(θ) - g(60)*sin(θ) + X
y(60) = 42 + 60*sin(θ) + g(60)*cos(θ)
```

This is an **overdetermined system solvable directly** with
`scipy.optimize.least_squares` — no scanning of the whole curve, no KD-tree,
no population-based search.

## Method

1. Find the two extreme data points via PCA projection onto the
   principal axis.
2. Try both endpoint-label assignments (`(t=6,t=60)` vs. `(t=60,t=6)`) since
   PCA direction has a sign ambiguity — keep whichever gives the smaller
   residual.
3. Solve the 4-equation/3-unknown system with `least_squares`.

## Result

```
theta = 29.944 deg
M     = 0.02976
X     = 55.022
Residual norm = 0.039
```

This independently reproduces the GlobalOptima answer (θ=30°, M=0.03, X=55) to
within noise, using a completely different mathematical route.