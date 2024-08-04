import os,sys
from math import *
from ROOT import *

signalList = ["rinv0p9", "rinv0p5", "rinv0p1"]
bkgFile = TFile("output_multijet_GammaISR150_yStar0p8.root")
bkgHist = bkgFile.Get("rinv_ave_maos").Clone()
print(bkgHist.Integral())

outf = TFile("sOverB_effScan_Z500_GammaISR150_rinv_maos.root", "RECREATE")

for signal in signalList:
    print(signal)
    signalFile = TFile("output_Z500_GammaISR150_" + signal + "_yStar0p8.root")
    signalHist = signalFile.Get("rinv_ave_maos").Clone()
    print(signalHist.Integral())
    sOverBHist = TH1D(signal + "_Z500_ISR150_significance", signal + "_Z500_ISR150_significance", 20, 0, 1)
    effHit = bkgHist.Clone()
    effBkgHit = bkgHist.Clone()
    for i in range(0, 20):
        targeteff = 1 - 0.05 * i
        targetbin = 1
        for j in range(0, signalHist.GetNbinsX() + 1):
            signalCount = signalHist.Integral(signalHist.GetXaxis().FindBin(bkgHist.GetBinCenter(j)), signalHist.GetNbinsX() + 1)
            eff = signalCount/signalHist.Integral()
            if eff <= targeteff:
                targetbin = j
                break 
        bkg = bkgHist.Integral(j, sOverBHist.GetNbinsX() + 1)
        signalCount = signalHist.Integral(signalHist.GetXaxis().FindBin(bkgHist.GetBinCenter(j)), signalHist.GetNbinsX() + 1)
        if bkg:
            sOverBHist.SetBinContent(20 - i, signalCount/sqrt(bkg))
        else:
            sOverBHist.SetBinContent(20 - i, sOverBHist.GetBinContent(20 - i + 1)) 
        sOverBHist.SetBinError(i, 0)
    outf.cd()
    sOverBHist.Write()
    


