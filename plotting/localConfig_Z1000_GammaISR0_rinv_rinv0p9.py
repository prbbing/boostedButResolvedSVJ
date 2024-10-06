import os

name = "rinv_compare_Z1000_GammaISR0_rinv0p9"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 2.0,
  "Xmin"   : 0.0,
  "Ymin"   : 0,
  "Ymax"   : 1,
  "nameX"  : "Reco r_{inv}",
  "nameY"  : "Arbitrary Units",
  "name"   : name,
  "doLogy" : 0,
  "rebinFactor" : 4,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "p_{T}^{ISR} > 0 GeV",
  "lumi" : -1,
  "cme"  : 13,
  "relErrMax" : 99999,
  "scaleToData" : 0,
  "sort" : 1,
  "ratioYLabel" : "Ratio",
  "ratioYmin" : 0,
  "ratioYmax" : 2.0,
  "normalized" : 1,
}

if "bing" in os.environ["USER"]:
    dir = "/Users/adminbingxuanliu/Work/boostedButResolvedSVJ/jhep_version/"
else:
    dir = "."

compareSources = {
  "1" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR0_rinv0p9.root",
    "histPath"    :   ["rinv_xy_ave"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv} (m_{Z'} = 1.0 TeV, r_{inv} = 0.9)",
  },
  "2" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR0_rinv0p9.root",
    "histPath"    :   ["rinv_xy_ave_maos"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r'}_{inv} (m_{Z'} = 1.0 TeV, r_{inv} = 0.9)",
  },
  "3" : {
    "filePath"    :   dir+"/output_multijet_JetISR500.root",
    "histPath"    :   ["rinv_xy_ave"],
    "color"       :   13,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv} (Multijet)",
  },
  "4" : {
    "filePath"    :   dir+"/output_multijet_JetISR500.root",
    "histPath"    :   ["rinv_xy_ave_maos"],
    "color"       :   13,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r'}_{inv} (Multijet)",
  },
}
