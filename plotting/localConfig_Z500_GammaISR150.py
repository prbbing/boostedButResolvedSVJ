import os

name = "signif_vs_rT_Z500_GammaISR150"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 1,
  "Xmin"   : 0,
  "Ymin"   : 0,
  "Ymax"   : 30,
  "nameX"  : "r_{T}",
  "nameY"  : "S/#sqrt{B}",
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
    dir = "/Users/adminbingxuanliu/Work/boostedButResolvedSVJ/jhep_version/"
else:
    dir = "."

compareSources = {
  "1" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv_yStar0p8.root",
    "histPath"    :   ["signif_rT_Z500_GammaISR150_rinv0p1"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.1",
  },
  "2" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv_yStar0p8.root",
    "histPath"    :   ["signif_rT_Z500_GammaISR150_rinv0p5"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.5",
  },
  "3" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv_yStar0p8.root",
    "histPath"    :   ["signif_rT_Z500_GammaISR150_rinv0p9"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{inv} = 0.9",
  },
}
