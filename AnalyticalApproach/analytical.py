import numpy as np, pandas as pd
from scipy.optimize import least_squares

df = pd.read_csv('/Users/viswa/Desktop/PythonProject/Flam_AI/xy_data.csv')
pts = df[['x', 'y']].values

c = pts.mean(axis=0)
_, _, Vt = np.linalg.svd(pts - c)
proj = (pts - c) @ Vt[0]
p_lo, p_hi = pts[proj.argmin()], pts[proj.argmax()]

def residuals(params, p6, p60):
    th, M, X = params
    g6, g60 = np.exp(M*6)*np.sin(1.8), np.exp(M*60)*np.sin(18.0)
    x6, y6  = 6*np.cos(th)  - g6*np.sin(th)  + X, 42 + 6*np.sin(th)  + g6*np.cos(th)
    x60, y60 = 60*np.cos(th) - g60*np.sin(th) + X, 42 + 60*np.sin(th) + g60*np.cos(th)
    return [x6-p6[0], y6-p6[1], x60-p60[0], y60-p60[1]]

best = None
for p6, p60 in [(p_lo, p_hi), (p_hi, p_lo)]:
    sol = least_squares(residuals, x0=[np.radians(25), 0.0, 50], args=(p6, p60),
                         bounds=([0, -0.05, 0], [np.radians(50), 0.05, 100]))
    if best is None or np.linalg.norm(sol.fun) < np.linalg.norm(best.fun):
        best = sol

th, M, X = best.x
print(f"Boundary-based estimate: theta={np.degrees(th):.3f} deg, M={M:.5f}, X={X:.3f}")
print(f"Residual norm: {np.linalg.norm(best.fun):.5f}")