from localConfig_Z1000_GammaISR500_mass_rinv0p9 import *
  
name = "mass_compare_Z1000_GammaISR500_rinv0p1"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 0.15
taskSetup["masterLabel"] = "Z' (0.5 TeV), r_{inv} = 0.1, p_{T}^{ISR} > 500 GeV"
 
for k in compareSources:
    compareSources[k]["filePath"] = dir+"/output_Z1000_GammaISR500_rinv0p1.root"
