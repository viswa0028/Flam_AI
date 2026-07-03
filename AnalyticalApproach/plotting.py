import numpy as np, pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../xy_data.csv')

theta, M, X = np.radians(29.944), 0.02976, 55.022
t = np.linspace(6, 60, 2000)
g = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
xm = t * np.cos(theta) - g * np.sin(theta) + X
ym = 42 + t * np.sin(theta) + g * np.cos(theta)

plt.figure(figsize=(7, 7))
plt.scatter(df.x, df.y, s=4, alpha=0.4, label='data points')
plt.plot(xm, ym, color='red', lw=2, label='predicted curve')
plt.gca().set_aspect('equal')
plt.legend()
plt.title("Analytical Approach")
plt.savefig('analytical.png', dpi=120, bbox_inches='tight')