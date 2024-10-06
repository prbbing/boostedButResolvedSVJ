from localConfig_Z1000_GammaISR500_mass_rinv0p9 import *
  
name = "mass_var_compare_Z500_GammaISR150_rinv0p5"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 0.20
taskSetup["masterLabel"] = "Z' (0.5 TeV), r_{inv} = 0.5, p_{T}^{ISR} > 150 GeV"
 
for k in compareSources:
    compareSources[k]["filePath"] = dir+"/output_Z500_GammaISR150_rinv0p5.root"
