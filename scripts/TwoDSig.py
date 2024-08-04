import os,sys
from ROOT import *

outf = TFile("Z1000_ISR500_TwoD_Sig_rinv0p5.root","RECREATE")
bkgf = TFile("output_multijet_JetISR500_yStar0p8.root")
bkgHist = bkgf.Get("rinv_ave_maosjj").Clone() 
bkgHist.Rebin2D(10,4)

#sigf_1 = TFile("output_Z1000_JetISR500_rinv0p9_yStar0p8.root")
#sigHist_1 = sigf_1.Get("rinv_ave_maosjj").Clone()
#sigf_2 = TFile("output_Z1000_JetISR500_rinv0p5_yStar0p8.root")
#sigHist_2 = sigf_2.Get("rinv_ave_maosjj").Clone()
sigf_3 = TFile("output_Z1000_JetISR500_rinv0p5_yStar0p8.root")
sigHist_3 = sigf_3.Get("rinv_ave_maosjj").Clone()
#sigHist_3.Add(sigHist_3, sigHist_2, 1, 1)
#sigHist_3.Add(sigHist_3, sigHist_1, 1, 1)
sigHist_3.Rebin2D(10,4)
sigHist = sigHist_3.Clone()

newHist = sigHist.Clone()

for i in range(1,  newHist.GetNbinsX() + 1):
    for j in range(1,  newHist.GetNbinsY() + 1):
        nBin =  newHist.FindBin(newHist.GetXaxis().GetBinCenter(i), newHist.GetYaxis().GetBinCenter(j))
        significance = 0
        if bkgHist.GetBinContent(nBin):
            significance = sigHist.GetBinContent(nBin)/sqrt(bkgHist.GetBinContent(nBin))
        newHist.SetBinContent(nBin, significance)

outf.cd()
newHist.Write()
 
