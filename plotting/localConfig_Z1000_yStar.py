import os

name = "yStar_compare_Z1000"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 2.5,
  "Xmin"   : 0,
  "Ymin"   : 0.01,
  "Ymax"   : 100,
  "nameX"  : "|y*|",
  "nameY"  : "Arbitrary Units",
  "name"   : name,
  "doLogy" : 1,
  "rebinFactor" : 2,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "Z' (1.0 TeV), Jet ISR",
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
    "filePath"    :   dir+"/output_Z1000_GammaISR0_rinv0p1.root",
    "histPath"    :   ["yStar"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.1, p_{T}^{ISR} > 0 GeV",
  },
  "2" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p1.root",
    "histPath"    :   ["yStar"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.1, p_{T}^{ISR} > 500 GeV",
  },
  "3" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR0_rinv0p5.root",
    "histPath"    :   ["yStar"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.5, p_{T}^{ISR} > 0 GeV",
  },
  "4" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p5.root",
    "histPath"    :   ["yStar"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.5, p_{T}^{ISR} > 500 GeV",
  },
  "5" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR0_rinv0p9.root",
    "histPath"    :   ["yStar"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.9, p_{T}^{ISR} > 0 GeV",
  },
  "6" : {
    "filePath"    :   dir+"/output_Z1000_GammaISR500_rinv0p9.root",
    "histPath"    :   ["yStar"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.9, p_{T}^{ISR} > 500 GeV",
  },
}
