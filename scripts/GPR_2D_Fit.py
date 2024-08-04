import numpy as np
import os,sys
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd 
import uproot

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.model_selection import train_test_split

histograms = uproot.open("two_d_rebinned_Z1000_0p1.root")
arr = histograms["bkg"].to_boost().to_numpy()

z_values = arr[0]
x_edges = arr[1]
y_edges = arr[2]

x_bincenters = (x_edges[1:] + x_edges[:-1])/2
y_bincenters = (y_edges[1:] + y_edges[:-1])/2

x = x_bincenters.reshape(-1,1)
y = y_bincenters.reshape(-1,1)
x_grid, y_grid = np.meshgrid(x.reshape(-1), y.reshape(-1))

z = z_values.T

# Convert to column vectors for scikit-learn
X = np.column_stack((x_grid.reshape(-1), np.log(y_grid.reshape(-1))))
Z = z.reshape(-1, 1)

# Set up the kernel: 
# Radial basis function with two length scales for smooth variations
# and white kernel to account for noise
guess_l = (1, 2)  
bounds_l = ((0.2, 2), (0.1, 20))  
const_n = 1.0  
bounds_c = (1e-5, 10e12)  # Bounds for noise
kernel = RBF(  length_scale=guess_l, length_scale_bounds=bounds_l) * ConstantKernel(constant_value=const_n, constant_value_bounds=bounds_c)

#X_train, X_test, Y_train, Y_test = train_test_split(X, Z, test_size=0.00)
X_train = X
Y_train = np.log(Z)
alpha_array = 2*pow(Z,0.5).reshape(-1)/(Z.reshape(-1) * np.log(Z).reshape(-1))
#alpha_array = pow(Z,0.5).reshape(-1)/Z.reshape(-1)
#alpha_array = 0.5*pow(Z,0.5).reshape(-1)/Z.reshape(-1)
alpha_array[np.abs(alpha_array) == np.inf] = 1
alpha_array[np.isnan(alpha_array)] = 1
Y_train[np.abs(Y_train) == np.inf] = 0.00000001
Y_train[np.isnan(Y_train)] = 1
gpr = GaussianProcessRegressor(kernel,  alpha=alpha_array, n_restarts_optimizer=10000)
gpr.fit(X_train, Y_train)

print(gpr.kernel_)

# Predict and reshape back to grid for plotting
Zfit, Zstd = gpr.predict(X, return_std=True)
zstd = np.exp(Zstd.reshape(x_grid.shape))
zfit = np.exp(Zfit.reshape(x_grid.shape))
# Plot posterior mean
significance = (z - zfit)/pow(zfit,0.5)
print((z - zfit)/pow(zfit,0.5))

# Set up figure
fig, ax = plt.subplots(figsize=(6.,4.))
ax.set_ylim((400, 3000))
ax.set_xlim((-300, 1500))
ax.grid(False)
im = plt.imshow(significance,interpolation='none', extent=[-300,1500,400,3000], vmin=-3, vmax=3)
plt.xticks([-300,0,300,600,900,1200,1500], [-0.2,0,0.2,0.4,0.6,0.8,1.0])
cbar = plt.colorbar(im, label = 'significance')
ax.set_title('multijet')
ax.set_xlabel('$\overline{r}_{\mathrm{inv}}$', loc='right')
ax.set_ylabel('$m_{\mathrm{MAOS}}$ [GeV]', loc='top')
plt.tight_layout()
plt.savefig("gpr_posterior_mean_Z1000_0p1.eps")
plt.show()
sys.exit(0)

# Plot posterior standard deviation

# Set up figure
fig, ax = plt.subplots(figsize=(6.,4.))
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_xlim((-5, 5))
ax.set_ylim((-5, 5))
ax.set_aspect("equal")
ax.set_xticks((-5, 0, 5))
ax.set_yticks((-5, 0, 5))
ax.grid(False)

# Do the plotting
ax.plot(*X_train.T, "o", color="C1")  # Training samples
lev = np.linspace(6.0, 16.0, 11)
hc = ax.contourf(x, y, zstd, lev)  # Posterior std
for hci in hc.collections:
    hci.set_edgecolor("face")

# Colorbar
hcb = plt.colorbar(hc)
hcb.ax.grid(False)
hcb.set_label("Posterior standard deviation")

# Write out
plt.tight_layout()
plt.savefig("gpr_posterior_std.svg")

