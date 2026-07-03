import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("==================================================")
    print("Running Algebraic Decoupling...")
    print("==================================================")
    sys.path.append(os.path.abspath('AlgebraicDecoupling'))
    import algebraic_decoupling as ad

    print("\n==================================================")
    print("Running Global Optimization (may take ~30 seconds)...")
    print("==================================================")
    sys.path.append(os.path.abspath('Globaloptim'))
    import globaloptim as go

    # Prepare figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)

    # --- Plot 1: Algebraic Decoupling ---
    ax1.scatter(ad.x, ad.y, s=5, c='blue', alpha=0.3, label='Data Points')
    ax1.plot(ad.xm, ad.ym, c='red', linewidth=2, label='Predicted Curve')
    ad_title = f"Algebraic Decoupling\n$\\theta$ = {np.degrees(ad.theta_est):.3f}°, M = {ad.M_est:.4f}, X = {ad.X_est:.3f}"
    ax1.set_title(ad_title, fontsize=12)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- Plot 2: Global Optimization ---
    ax2.scatter(go.data_pts[:, 0], go.data_pts[:, 1], s=5, c='blue', alpha=0.3, label='Data Points')
    go_model_pts = go.model_xy(go.t_uniform, np.radians(go.theta_deg), go.M_est, go.X_est)
    ax2.plot(go_model_pts[:, 0], go_model_pts[:, 1], c='red', linewidth=2, label='Predicted Curve')
    go_title = f"Global Optimization\n$\\theta$ = {go.theta_deg:.3f}°, M = {go.M_est:.4f}, X = {go.X_est:.3f}"
    ax2.set_title(go_title, fontsize=12)
    ax2.set_xlabel('x')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparison_plot.png', dpi=150)
    print("\n==================================================")
    print("Plot successfully saved to comparison_plot.png!")
    print("==================================================")
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    main()
