import os,sys
from math import *
from ROOT import *

massList = ["Z1000_JetISR500","Z500_GammaISR150"]
signalList = ["rinv0p9", "rinv0p5", "rinv0p1"]
rinvList = ["rT","rTmaos","rTdecomp","rinv_x_ave","rinv_y_ave","rinv_xy_ave","rinv_t_ave"]
rinvList = rinvList + [rinv+"_maos" for rinv in rinvList if rinv.startswith("rinv")]
# for mass window
mvar = "maosjj"
# for sOverB vs eff
nbins = 20

def getHist(file,hname,proc,mrange=None,mvar=None):
    cname = proc
    if mrange is not None:
        cname += "_"+mvar
    hist = file.Get(hname).Clone(cname)
    if mrange is not None:
        b1 = hist.GetYaxis().FindBin(mrange[0])
        b2 = hist.GetYaxis().FindBin(mrange[1])
        hist = hist.ProjectionX(proc, b1, b2)
    if not hname.startswith("rT"):
        hist.Rebin(2)
    return hist

for mass in massList:
    print(mass)
    mzprime = float(mass.split('_')[0][1:])
    mmin = 1/2*mzprime
    mmax = 3/2*mzprime
    outf = TFile("sOverB_"+mass+"_rinv.root", "RECREATE")
    bkgFile = TFile("output_multijet_"+mass.split('_')[1]+".root")
    for signal in signalList:
        print(signal)
        sigFile = TFile("output_"+ mass + "_" + signal + ".root")
        for rinv in rinvList:
            suff = "_"+rinv+"_"+mass+"_"+signal
            hname = rinv+"_"+mvar
            print(hname)
            bkgHist = getHist(bkgFile,hname,"bkg"+suff,mrange=(mmin,mmax),mvar=mvar)
            sigHist = getHist(sigFile,hname,"sig"+suff,mrange=(mmin,mmax),mvar=mvar)
            sOverBHist = bkgHist.Clone("signif"+suff)
            sOverBEffHist = TH1D("signif_eff"+suff,"signif_eff"+suff,nbins,0,1)
            effHist = bkgHist.Clone("eff"+suff)
            effBkgHist = bkgHist.Clone("eff"+suff.replace(rinv,rinv+"_multijet"))
            for i in range(1, sOverBHist.GetNbinsX() + 1):
                signalCount = sigHist.Integral(sigHist.GetXaxis().FindBin(bkgHist.GetBinCenter(i)), sigHist.GetNbinsX() + 1)
                bkg = bkgHist.Integral(i, sOverBHist.GetNbinsX() + 1)
                eff = signalCount/sigHist.Integral()
                effBkg = bkg/bkgHist.Integral()
                if bkg > 0:
                    sOverBHist.SetBinContent(i, signalCount/sqrt(bkg))
                else:
                    sOverBHist.SetBinContent(i, sOverBHist.GetBinContent(i - 1))
                sOverBHist.SetBinError(i, 0)
                effHist.SetBinContent(i, eff)
                effHist.SetBinError(i, 0)
                effBkgHist.SetBinContent(i, effBkg)
                effBkgHist.SetBinError(i, 0)
            # another loop to pick out values for sOverB vs eff
            for i in range(0,nbins):
                targeteff = 1 - 0.05 * i
                targetbin = 1
                for j in range(1, effHist.GetNbinsX() + 1):
                    if effHist.GetBinContent(j) <= targeteff:
                        targetbin = j
                        break
                sOverBEffHist.SetBinContent(nbins - i, sOverBHist.GetBinContent(targetbin))
                sOverBEffHist.SetBinError(nbins - i, 0)
            outf.cd()
            sOverBHist.Write()
            sOverBEffHist.Write()
            bkgHist.Write()
            sigHist.Write()
            effHist.Write()
            effBkgHist.Write()
    outf.Close()
