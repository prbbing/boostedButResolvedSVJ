import os

name = "mass_compare_Z1000_GammaISR500_rinv0p9"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 1600,
  "Xmin"   : 200,
  "Ymin"   : 0,
  "Ymax"   : 1,
  "nameX"  : "Reco Mass [GeV]",
  "nameY"  : "Arbitrary Units",
  "name"   : name,
  "doLogy" : 0,
  "rebinFactor" : 1,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "Z' (1.0 TeV), r_{inv} = 0.9, p_{T}^{ISR} > 500 GeV",
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
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p9.root",
    "histPath"    :   ["mTjj"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "m_{T}",
  },
  "2" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p9.root",
    "histPath"    :   ["mjjRecomp"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "m_{decomp}",
  },
  "3" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p9.root",
    "histPath"    :   ["maosjj"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "m_{MAOS}",
  },
}
