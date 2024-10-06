from localConfig_Z1000_GammaISR500_rinv_rinv0p9 import *
  
name = "rinv_var_compare_Z500_GammaISR150_rinv0p5"
outputPath = name+".root"
taskSetup["name"] = name
taskSetup["Ymax"] = 0.45
taskSetup["masterLabel"] = "p_{T}^{ISR} > 150 GeV"
 
for k in compareSources:
    if "multijet" not in compareSources[k]["filePath"]:
        compareSources[k]["filePath"] = dir+"/output_Z500_GammaISR150_rinv0p5.root"
        compareSources[k]["legendLabel"] = "#bar{r'}_{inv} (m_{Z'} = 0.5 TeV, r_{inv} = 0.5)"
    if "multijet" in compareSources[k]["filePath"]:
        compareSources[k]["filePath"] = dir+"/output_multijet_GammaISR150.root"
