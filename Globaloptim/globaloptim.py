import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution, minimize
from scipy.spatial import cKDTree
import time

df = pd.read_csv('./xy_data.csv')
data_pts = df[['x', 'y']].values
N_DATA = len(data_pts)

T_LO, T_HI = 6.0, 60.0
N_SAMPLE = 600           
t_uniform = np.linspace(T_LO, T_HI, N_SAMPLE)

data_tree = cKDTree(data_pts)

def model_xy(t, theta, M, X):
    g = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    xm = t * np.cos(theta) - g * np.sin(theta) + X
    ym = 42 + t * np.sin(theta) + g * np.cos(theta)
    return np.column_stack([xm, ym])

def chamfer_l1(params):
    theta_deg, M, X = params
    theta = np.radians(theta_deg)
    model_pts = model_xy(t_uniform, theta, M, X)

    model_tree = cKDTree(model_pts)
    d_data_to_model, _ = model_tree.query(data_pts, k=1, p=1)
    d_model_to_data, _ = data_tree.query(model_pts, k=1, p=1)

    return 0.5 * (d_data_to_model.mean() + d_model_to_data.mean())

bounds = [(0.0, 50.0), (-0.05, 0.05), (0.0, 100.0)]  

print("Global Search")
t0 = time.time()
result = differential_evolution(
    chamfer_l1, bounds,
    maxiter=150, popsize=25, tol=1e-8,
    mutation=(0.4, 1.5), recombination=0.8,
    seed=42, polish=False, workers=1, updating='immediate'
)

polished = minimize(chamfer_l1, result.x, method='Nelder-Mead',
                     options={'xatol': 1e-6, 'fatol': 1e-8, 'maxiter': 5000})

theta_deg, M_est, X_est = polished.x
final_err = chamfer_l1(polished.x)

print(f"theta = {theta_deg:.4f} deg")
print(f"M     = {M_est:.5f}")
print(f"X     = {X_est:.3f}")
print(f"L1 error = {final_err:.4f}")