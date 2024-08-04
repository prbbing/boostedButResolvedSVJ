import matplotlib.pyplot as plt
import numpy as np

x = np.array([])
y = np.array([])
area = np.array([]) 

x_1 = np.array([])
y_1 = np.array([])
area_1 = np.array([]) 

x_2 = np.array([])
y_2 = np.array([])
area_2 = np.array([]) 

f = open('log_qcd')

counter = 0
for line in f:
    if counter >= 20000:
      break
    if float(line.split(":")[1]) < 2000 and float(line.split(":")[0]) < 0.8 and float(line.split(":")[0]) > -0.8:
      x = np.append(x, float(line.split(":")[0]))
      y = np.append(y, float(line.split(":")[1]))
      area = np.append(area, 2)
      counter = counter + 1

counter = 0
f = open('log_Z1000_rinv0p9')
for line in f:
    if counter >= 5000:
      break
    if float(line.split(":")[1]) < 2000 and float(line.split(":")[0]) < 0.8 and float(line.split(":")[0]) > -0.8:
      x_1 = np.append(x_1, float(line.split(":")[0]))
      y_1 = np.append(y_1, float(line.split(":")[1]))
      area_1 = np.append(area_1, 2)
      counter = counter + 1

fig = plt.figure(1, figsize=(8, 6))
ax = fig.add_subplot(111)

qcd = ax.scatter(x, y, s=area, c="grey", alpha=1, label='multijet')
signal = ax.scatter(x_1, y_1, s=area_1, c="c", alpha=0.5, label='Z\' (1 TeV) $r_{\mathrm{inv}} = 0.9$')
lgd = ax.legend(handles=[qcd, signal],fontsize=14)

lgd.legend_handles[0]._sizes = [30]
lgd.legend_handles[1]._sizes = [30]
ax.set_xlabel("$\overline{r}_{\mathrm{inv}}$", fontsize=14)
ax.set_ylabel("$m_{\mathrm{MAOS}}$ [GeV]", fontsize=14)
ax.set_title("ISR jet $p_{\mathrm{T}} > 500$ GeV", loc = 'center', fontsize=20, pad=20)
ax.xaxis.set_label_coords(0.98, -0.08)
ax.yaxis.set_label_coords(-0.1, 0.88)
plt.savefig('scatter_ISR500.eps')
plt.show()

