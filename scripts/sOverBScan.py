import os,sys
from math import *
from ROOT import *

massList = ["Z1000_JetISR500","Z500_GammaISR150"]
signalList = ["rinv0p9", "rinv0p5", "rinv0p1"]
rinvList = ["rT","rinv_x_ave","rinv_y_ave","rinv_xy_ave","rinv_t_ave"]
rinvList = rinvList + [rinv+"_maos" for rinv in rinvList if rinv.startswith("rinv")]

for mass in massList:
    outf = TFile("sOverB_"+mass+"_rinv.root", "RECREATE")
    bkgFile = TFile("output_multijet_"+mass.split('_')[1]+".root")
    for signal in signalList:
        print(signal)
        signalFile = TFile("output_"+ mass + "_" + signal + ".root")
        for rinv in rinvList:
            bkgHist = bkgFile.Get(rinv).Clone()
            bkgHist.Rebin(2)
            print(bkgHist.Integral())
            signalHist = signalFile.Get(rinv).Clone()
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
            sOverBHist.SetName("signif_"+rinv+"_"+mass+"_"+signal)
            effHit.SetName("eff_"+rinv+"_"+mass+"_"+signal)
            effBkgHit.SetName("eff_"+rinv+"_multijet"+"_"+mass+"_"+signal)
            outf.cd()
            sOverBHist.Write()
            effHit.Write()
            effBkgHit.Write()
    outf.Close()
