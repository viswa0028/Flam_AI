# Approach 2: Direct Global Optimization

## Idea
The Algebraically Decoupling, is deeply flawed for finding accurate values. Because the variables are coupled through a non-linear model, separating them meant that the small approximation error from PCA the values are biased every subsequent step. This bias caused the internal consistency and caused our L1 error to be 3.8.

The fix is to stop decoupling entirely. Instead of using proxy equations, we directly optimize `θ`, `M`, and `X` **jointly** against the real scoring metric: the Chamfer-L1 distance. Since this objective function is full of local minima (due to the periodic sine waves), we use a global search algorithm rather than a local optimizer.

## How to run
```bash
python global_optim.py
```

## What it does
1. **Global Search:** Uses Differential Evolution (`scipy.optimize.differential_evolution`) to search the entire bounded parameter space. This avoids the trap of falling into a local minimum that a simple local optimizer would hit.
2. **Local Polish:** Once the global search narrows down the best region, it switches to a Nelder-Mead simplex search to find out the highest possible precision.
3. **Scoring:** The objective function densely samples the model curve and computes the symmetric nearest-neighbor L1 distance to the data using a KD-tree.

## Actual result when run
```text
theta = 30.0003 deg
M     = 0.03000
X     = 55.001
L1 error = 0.0305
```

## Why this happens (Fixing Approach 1's Mistakes)
This approach achieves a ~125x reduction in error (dropping from 3.8 to 0.03) because it fixes the two major flaws of Approach 1:
1. **No Staging Bias:** By estimating all three parameters simultaneously, no single stage can accumulate and pass along bias to the next stage.
2. **No Proxy Objectives:** We are directly minimizing the true L1 distance between the model and the scattered data points, ensuring that "good fit" is possible.

## Conclusion
While Algebraic Decoupling (Approach 1) was a useful attempt, it failed to provide accurate values. **Direct Global Optimization** is better for this problem. By exploring the entire parameter space and directly targeting the L1 metric, we sidestep the local-minima traps and staging biases, recovering what are very clearly the exact, round ground-truth parameters (`θ=30°`, `M=0.03`, `X=55`).