from localConfig_Z500_GammaISR150 import *

name = "signif_vs_rinv_xy_ave_Z1000_JetISR500"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 180
taskSetup["nameX"] = "#bar{r}_{inv}"
taskSetup["masterLabel"] = "Z' (1.0 TeV), p_{T}^{ISR} > 500 GeV"

for k in compareSources:
    compareSources[k]["filePath"] = dir+"/sOverB_Z1000_JetISR500_rinv_yStar0p8.root"
    compareSources[k]["histPath"] = [h.replace("Z500","Z1000").replace("GammaISR150","JetISR500").replace("rT","rinv_xy_ave") for h in compareSources[k]["histPath"]]
