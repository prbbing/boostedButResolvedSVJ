import os

name = "matching_compare_ISR500"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 3,
  "Xmin"   : 0,
  "Ymin"   : 0.01,
  "Ymax"   : 100,
  "nameX"  : "Matched Jet Pair",
  "nameY"  : "Arbitrary Units",
  "name"   : name,
  "doLogy" : 1,
  "rebinFactor" : 1,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "p_{T}^{ISR} > 500 GeV",
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
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p1_matching.root",
    "histPath"    :   ["closestPairToMet"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "Z' (1.0 TeV), r_{inv} = 0.1",
  },
  "2" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p5_matching.root",
    "histPath"    :   ["closestPairToMet"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "Z' (1.0 TeV), r_{inv} = 0.5",
  },
  "3" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p9_matching.root",
    "histPath"    :   ["closestPairToMet"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "Z' (1.0 TeV), r_{inv} = 0.9",
  },
}
