import numpy as np
import os,sys
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd 
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogFormatterMathtext
import uproot

histograms_bkg = uproot.open("two_d_rebinned.root")
arr_bkg = histograms_bkg["bkg"].to_boost().to_numpy()
histograms_sig = uproot.open("two_d_rebinned_z1000_0p1.root")
arr_sig = histograms_sig["bkg"].to_boost().to_numpy()

z_values_bkg = arr_bkg[0]
z_values_sig = arr_sig[0]
x_edges = arr_bkg[1]
y_edges = arr_bkg[2]

x_bincenters = (x_edges[1:] + x_edges[:-1])/2
y_bincenters = (y_edges[1:] + y_edges[:-1])/2

x = x_bincenters.reshape(-1,1)
y = y_bincenters.reshape(-1,1)
x_grid, y_grid = np.meshgrid(x.reshape(-1), y.reshape(-1))

z_bkg = z_values_bkg.T
z_sig = z_values_sig.T

significance =  (z_sig - z_bkg)/(pow(z_bkg, 0.5))

# Set up figure
fig, ax = plt.subplots(figsize=(6.,4.))
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_ylim((400, 2000))
ax.set_xlim((-600, 1000))
ax.grid(False)
im = plt.imshow(significance,interpolation='none', extent=[-600,1000,400,2000])
plt.xticks([-600,-400,-200,0,200,400,600,800,1000], [-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.0])
plt.colorbar(im)
ax.set_title('Significance: multijet + signal')
ax.set_xlabel('$\overline{r}_{\mathrm{inv}}$', loc='right')
ax.set_ylabel('$m_{\mathrm{MAOS}}$ [GeV]', loc='top')
plt.tight_layout()
plt.savefig("raw_sigificance_z1000")
plt.show()
sys.exit(0)
