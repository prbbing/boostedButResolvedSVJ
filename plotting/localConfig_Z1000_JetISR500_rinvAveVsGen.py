from localConfig_Z500_GammaISR150_rinvAveVsGen import *

name = "rinvAve_vs_gen_Z1000_JetISR500"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["masterLabel"] = "Z' (1.0 TeV), p_{T}^{ISR} > 500 GeV"
for k in compareSources:
    compareSources[k]["filePath"] = dir+"/rinvAveVsGen_Z1000_JetISR500.root"
