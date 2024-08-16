import os

name = "rinvAve_vs_gen_Z500_GammaISR150"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 1,
  "Xmin"   : 0,
  "Ymin"   : 0,
  "Ymax"   : 0.5,
  "nameX"  : "r_{inv}",
  "nameY"  : "Reco r_{inv}",
  "name"   : name,
  "doLogy" : 0,
  "rebinFactor" : 1,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "Z' (0.5 TeV), p_{T}^{ISR} > 150 GeV",
  "lumi" : -1,
  "cme"  : 13,
  "relErrMax" : 99999,
  "scaleToData" : 0,
  "sort" : 1,
  "ratioYLabel" : "Ratio",
  "ratioYmin" : 0,
  "ratioYmax" : 2.0,
  "normalized" : 0,
}

if "bing" in os.environ["USER"]:
    dir = "/Users/adminbingxuanliu/Work/boostedButResolvedSVJ/realSel"
else:
    dir = "."

compareSources = {
  "1" : {
    "filePath"    :   dir+"/rinvAveVsGen_Z500_GammaISR150.root",
    "histPath"    :   ["rinv_xy_ave"],
    "color"       :   9,
    "style"       :   20,
    "drawOption"  :   "pzl",
    "legendLabel" :   "#bar{r}_{inv}",
  },
  "2" : {
    "filePath"    :   dir+"/rinvAveVsGen_Z500_GammaISR150.root",
    "histPath"    :   ["rinv_xy_ave_maos"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "pzl",
    "legendLabel" :   "#bar{r}_{inv}^{MAOS}",
  },
}
