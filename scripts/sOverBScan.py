import os,sys
from math import *
from ROOT import *

signalList = ["rinv0p9", "rinv0p5", "rinv0p1"]
#bkgFile = TFile("output_multijet_GammaISR150_yStar0p8.root")
bkgFile = TFile("output_multijet_JetISR500_yStar0p8.root")
bkgHist = bkgFile.Get("rinv_ave").Clone()
bkgHist.Rebin(2)
print(bkgHist.Integral())

#outf = TFile("sOverB_Z500_GammaISR150_rT.root", "RECREATE")
outf = TFile("sOverB_Z1000_JetISR500_rinv.root", "RECREATE")

for signal in signalList:
    print(signal)
    #signalFile = TFile("output_Z500_GammaISR150_" + signal + "_yStar0p8.root")
    signalFile = TFile("output_Z1000_JetISR500_" + signal + "_yStar0p8.root")
    signalHist = signalFile.Get("rinv_ave").Clone()
    signalHist.Rebin(2)
    print(signalHist.Integral())
    sOverBHist = bkgHist.Clone()
    effHit = bkgHist.Clone()
    effBkgHit = bkgHist.Clone()
    for i in range(1, sOverBHist.GetNbinsX() + 1):
        signalCount = signalHist.Integral(signalHist.GetXaxis().FindBin(bkgHist.GetBinCenter(i)), signalHist.GetNbinsX() + 1)
        bkg = bkgHist.Integral(i, sOverBHist.GetNbinsX() + 1)
        eff = signalCount/signalHist.Integral()
        effBkg = bkg/bkgHist.Integral()
        if bkg > 0:
            sOverBHist.SetBinContent(i, signalCount/sqrt(bkg))
        else:
            sOverBHist.SetBinContent(i, sOverBHist.GetBinContent(i - 1)) 
        sOverBHist.SetBinError(i, 0)
        effHit.SetBinContent(i, eff)
        effHit.SetBinError(i, 0)
        effBkgHit.SetBinContent(i, effBkg)
        effBkgHit.SetBinError(i, 0)
    sOverBHist.SetName(signal + "_Z1000_ISR500_significance")
    effHit.SetName(signal + "_Z1000_ISR500_eff")
    effBkgHit.SetName("multijet_Z1000_ISR500_eff")
    outf.cd()
    sOverBHist.Write()
    effHit.Write()
    effBkgHit.Write()
    


