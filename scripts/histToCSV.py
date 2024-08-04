from ROOT import *

histograms_sig = TFile("realSel/output_Z1000_JetISR500_rinv0p9_yStar0p8.root")
histograms_bkg = TFile("realSel/output_multijet_JetISR500_yStar0p8.root")
out_f = TFile("two_d_rebinned_Z1000_0p1.root", "RECREATE")
hist_bkg = histograms_bkg.Get("rinv_ave_maosjj").Clone()
hist_sig = histograms_sig.Get("rinv_ave_maosjj").Clone()
hist_bkg.Sumw2()
hist_bkg.Add(hist_bkg, hist_sig, 1.0, 0.1)
hist_bkg.RebinX(10)
hist_bkg.RebinY(4)
newHist = TH2D("bkg","bkg",6,-0.2,1.0, 13,400,3000)

for i in range(1, newHist.GetNbinsX() + 1):
    for j in range(1, newHist.GetNbinsY() + 1):
        oldBin = hist_bkg.FindBin(newHist.GetXaxis().GetBinCenter(i), newHist.GetYaxis().GetBinCenter(j))
        newHist.SetBinContent(newHist.FindBin(newHist.GetXaxis().GetBinCenter(i), newHist.GetYaxis().GetBinCenter(j)) , hist_bkg.GetBinContent( oldBin))

out_f.cd()
newHist.Write()
out_f.Close()



