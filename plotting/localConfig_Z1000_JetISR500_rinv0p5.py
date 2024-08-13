from localConfig_Z1000_JetISR500_rinv0p9 import *

name = "sig_vs_eff_Z1000_JetISR500_rinv0p5"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 80
taskSetup["masterLabel"] = "Z' (1.0 TeV), r_{inv} = 0.5, p_{T}^{ISR} > 500 GeV"

for k in compareSources:
    compareSources[k]["histPath"] = [h.replace("rinv0p9","rinv0p5") for h in compareSources[k]["histPath"]]
