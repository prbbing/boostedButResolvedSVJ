from localConfig_Z1000_GammaISR500_rinv_rinv0p9 import *
  
name = "rinv_compare_Z1000_GammaISR500_rinv0p5"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["masterLabel"] = "Z' (1.0 TeV), r_{inv} = 0.5, p_{T}^{ISR} > 500 GeV"
 
for k in compareSources:
    if "multijet" not in compareSources[k]["filePath"]:
        compareSources[k]["filePath"] = dir+"/output_Z1000_GammaISR500_rinv0p5.root"
