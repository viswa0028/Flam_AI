# Algebraic Decoupling

## Idea
Since row order is not that useful here, we tried to find a way to decouple the rotation angle `θ`, the translation `X`, and the shape parameter `M` without knowing the time variable `t` for each point. We exploit the variance of the data: because `t` ranges broadly while the oscillating function remains relatively bounded, the dominant direction (principal axis) of the point cloud roughly aligns with `θ`. By projecting the data onto these PCA-derived axes, we separate rotation from shape, turning the problem into a simpler non-linear regression to solve for `M`, and eventually calculating the horizontal shift `X` by back-substitution.

## How to run
```bash
python algebraic_decoupling.py
```

## What it does
Runs Principal Component Analysis (PCA) to estimate `θ`, projects the data to decouple the rotation, and uses a curve fit regression to estimate `M`. Finally, it computes `X` and a `y`-intercept consistency check. It then densely samples the fitted curve over `t` and uses a KD-tree to calculate the L1 nearest-neighbor distance metric between the real data and the model.

## Actual result when run
```
PCA-estimated theta = 28.4831
M = 0.02565, c = 43.354, sign = -0.9
X = 45.737  

theta = 28.4831
M     = 0.02565
X     = 45.737
Mean L1 = 3.8093
Mean L1 = 3.7871
Symmetric mean L1 error = 3.7982
```

## Why high error:
The PCA is not working out because of the orthogonal deviation of e^|M(t)|sin(0.3t) which is deteministic oscillation function. Here the oscillations are not getting cancelled out so the error is getting higher.
And also if there are any outliers the L2 optimization would give mathematically optimal answer than L1 optimization.

## Conclusion
**We cannot rely purely on algebraic decoupling for high precision here** — it depends on the approximation that the curve's principal axis perfectly maps to `t`. This approach is a good one but it does not find the most optimal output for us. Hence we need to work with another approach for some what more optimal answer.
