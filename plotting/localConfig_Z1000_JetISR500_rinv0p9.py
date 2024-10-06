from localConfig_Z500_GammaISR150_rinv0p9 import *

name = "sig_vs_eff_Z1000_JetISR500_rinv0p9"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 150
taskSetup["masterLabel"] = "Z' (1.0 TeV), r_{inv} = 0.9, p_{T}^{ISR} > 500 GeV"

for k in compareSources:
    compareSources[k]["filePath"] = dir+"/sOverB_Z1000_JetISR500_rinv_yStar0p8.root"
    compareSources[k]["histPath"] = [h.replace("Z500","Z1000").replace("GammaISR150","JetISR500") for h in compareSources[k]["histPath"]]
