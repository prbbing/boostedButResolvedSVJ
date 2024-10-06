import os,sys
import ROOT as r

outf = r.TFile("crossSection_Z1000.root", "RECREATE")

xs = r.TH1D("xs","xs", 6, 0, 6)
xsTimesEff_rinv0p1 = r.TH1D("xsTimesEff_rinv0p1","xsTimesEff_rinv0p1", 6, 0, 6)
xsTimesEff_rinv0p5 = r.TH1D("xsTimesEff_rinv0p5","xsTimesEff_rinv0p5", 6, 0, 6)
xsTimesEff_rinv0p9 = r.TH1D("xsTimesEff_rinv0p9","xsTimesEff_rinv0p9", 6, 0, 6)

xs.SetBinContent(1, 44.1*5.76/53.4)
xs.SetBinContent(2, 5.9 *5.76/53.4 )
xs.SetBinContent(3, 1.86*5.76/53.4)
xs.SetBinContent(4, 0.75*5.76/53.4)
xs.SetBinContent(5, 0.37*5.76/53.4)
xs.SetBinContent(6, 0.42*5.76/53.4)

xsTimesEff_rinv0p1.SetBinContent(1, 1.88 *5.76/53.4)
xsTimesEff_rinv0p1.SetBinContent(2, 0.49*5.76/53.4)
xsTimesEff_rinv0p1.SetBinContent(3, 0.26*5.76/53.4)
xsTimesEff_rinv0p1.SetBinContent(4, 0.18*5.76/53.4)
xsTimesEff_rinv0p1.SetBinContent(5, 0.13*5.76/53.4)
xsTimesEff_rinv0p1.SetBinContent(6, 0.29*5.76/53.4)

xsTimesEff_rinv0p5.SetBinContent(1, 1.28*5.76/53.4)
xsTimesEff_rinv0p5.SetBinContent(2, 0.26*5.76/53.4)
xsTimesEff_rinv0p5.SetBinContent(3, 0.15*5.76/53.4)
xsTimesEff_rinv0p5.SetBinContent(4, 0.10*5.76/53.4)
xsTimesEff_rinv0p5.SetBinContent(5, 0.09*5.76/53.4)
xsTimesEff_rinv0p5.SetBinContent(6, 0.28*5.76/53.4)

xsTimesEff_rinv0p9.SetBinContent(1, 0.78*5.76/53.4)
xsTimesEff_rinv0p9.SetBinContent(2, 0.18*5.76/53.4)
xsTimesEff_rinv0p9.SetBinContent(3, 0.07*5.76/53.4)
xsTimesEff_rinv0p9.SetBinContent(4, 0.06*5.76/53.4)
xsTimesEff_rinv0p9.SetBinContent(5, 0.07*5.76/53.4)
xsTimesEff_rinv0p9.SetBinContent(6, 0.27*5.76/53.4)

outf.cd()
xs.Write()
xsTimesEff_rinv0p1.Write()
xsTimesEff_rinv0p5.Write()
xsTimesEff_rinv0p9.Write()

outf.Close()
