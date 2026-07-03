import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.spatial import cKDTree
df = pd.read_csv('./xy_data.csv')
x = df.x.values
y = df.y.values
N = len(x)

pts = np.column_stack([x, y])
centroid = pts.mean(axis=0)
pts_c = pts - centroid
cov = np.cov(pts_c.T)
eigval, eigvec = np.linalg.eigh(cov)
order = np.argsort(eigval)[::-1]
eigval, eigvec = eigval[order], eigvec[:, order]

principal_axis = eigvec[:, 0]
minor_axis = eigvec[:, 1]

theta_raw = np.arctan2(principal_axis[1], principal_axis[0])

theta_candidates = [theta_raw, theta_raw + np.pi, theta_raw - np.pi]
theta_est = None
for cand in theta_candidates:
    deg = np.degrees(cand) % 360
    if 0 < deg < 50:
        theta_est = np.radians(deg)
        break
if theta_est is None:
    theta_est = theta_raw  

print(f"PCA-estimated theta = {np.degrees(theta_est):.4f}")


dir_t = np.array([np.cos(theta_est), np.sin(theta_est)])
dir_g = np.array([-np.sin(theta_est), np.cos(theta_est)])
u = pts_c @ dir_t
v = pts_c @ dir_g  

def g_model(u, M, c, s):
    t = u + c
    return s * np.exp(M * np.abs(t)) * np.sin(0.3 * t)

best = None
for s0 in (1.0, -1.0):                  
    for c0 in np.linspace(-40, 40, 9):  
        try:
            popt, _ = curve_fit(
                g_model, u, v, p0=[0.0, c0, s0],
                bounds=([-0.05, -100, -1.5], [0.05, 100, 1.5]),
                maxfev=20000,
            )
            resid = np.sum((g_model(u, *popt) - v) ** 2)
            if best is None or resid < best[0]:
                best = (resid, popt)
        except Exception:
            continue

resid, (M_est, c_est, s_est) = best
print(f"M = {M_est:.5f}, c = {c_est:.3f}, sign = {s_est:.1f}")

t_est = u + c_est

g_est = np.exp(M_est * np.abs(t_est)) * np.sin(0.3 * t_est)
x_model_notrans = t_est * np.cos(theta_est) - g_est * np.sin(theta_est)
y_model_notrans = t_est * np.sin(theta_est) + g_est * np.cos(theta_est)

X_est = np.mean(x - x_model_notrans)
Y0_est = np.mean(y - y_model_notrans)   
print(f"X = {X_est:.3f}")
def model_xy(t, theta, M, X):
    g = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    xm = t * np.cos(theta) - g * np.sin(theta) + X
    ym = 42 + t * np.sin(theta) + g * np.cos(theta)
    return xm, ym

t_uniform = np.linspace(6, 60, 2000)
xm, ym = model_xy(t_uniform, theta_est, M_est, X_est)
model_pts = np.column_stack([xm, ym])

tree = cKDTree(model_pts)
dist_data_to_model, _ = tree.query(pts, k=1)
l1_data_to_model = np.mean(dist_data_to_model)

tree2 = cKDTree(pts)
dist_model_to_data, _ = tree2.query(model_pts, k=1)
l1_model_to_data = np.mean(dist_model_to_data)

print(f"theta = {np.degrees(theta_est):.4f} deg")
print(f"M     = {M_est:.5f}")
print(f"X     = {X_est:.3f}")
print(f"Mean L1 = {l1_data_to_model:.4f}")
print(f"Mean L1 = {l1_model_to_data:.4f}")
print(f"Symmetric mean L1 error = {(l1_data_to_model+l1_model_to_data)/2:.4f}")
