import os

name = "sig_vs_eff_Z500_GammaISR150_rinv0p9"
outputPath = name+".root"

taskSetup = {
  "Xmax"   : 1,
  "Xmin"   : 0,
  "Ymin"   : 0,
  "Ymax"   : 30,
  "nameX"  : "Efficiency",
  "nameY"  : "S/#sqrt{B}",
  "name"   : name,
  "doLogy" : 0,
  "rebinFactor" : 1,
  "doFraction"  : 0,
  "doRatio" : 0,
  "masterLabel" : "Z' (0.5 TeV), r_{inv} = 0.9, p_{T}^{ISR} > 150 GeV",
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
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rT_Z500_GammaISR150_rinv0p9"],
    "color"       :   1,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{T} selection",
  },
  "2" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rTmaos_Z500_GammaISR150_rinv0p9"],
    "color"       :   15,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "r_{T}^{maos} selection",
  },
  "3" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rinv_xy_ave_Z500_GammaISR150_rinv0p9"],
    "color"       :   9,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv}^{(xy)} selection",
  },
  "4" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rinv_t_ave_Z500_GammaISR150_rinv0p9"],
    "color"       :   8,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv}^{(T)} selection",
  },
  "5" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rinv_xy_ave_maos_Z500_GammaISR150_rinv0p9"],
    "color"       :   46,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv}^{MAOS (xy)} selection",
  },
  "6" : {
    "filePath"    :   dir+"/sOverB_Z500_GammaISR150_rinv.root",
    "histPath"    :   ["signif_eff_rinv_t_ave_maos_Z500_GammaISR150_rinv0p9"],
    "color"       :   42,
    "style"       :   21,
    "drawOption"  :   "histo",
    "legendLabel" :   "#bar{r}_{inv}^{MAOS (T)} selection",
  },
}
