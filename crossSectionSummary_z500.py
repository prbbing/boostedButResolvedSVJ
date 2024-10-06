import os,sys
from ROOT import *

outf = TFile("crossSection_Z500.root", "RECREATE")

xs = TH1D("xs","xs", 6, 0, 6)
xsTimesEff_rinv0p1 = TH1D("xsTimesEff_rinv0p1","xsTimesEff_rinv0p1", 6, 0, 6)
xsTimesEff_rinv0p5 = TH1D("xsTimesEff_rinv0p5","xsTimesEff_rinv0p5", 6, 0, 6)
xsTimesEff_rinv0p9 = TH1D("xsTimesEff_rinv0p9","xsTimesEff_rinv0p9", 6, 0, 6)

xs.SetBinContent(1, 352.8 * 86.511/397)
xs.SetBinContent(2, 31.02 * 86.511/397)
xs.SetBinContent(3, 8.35 * 86.511/397)
xs.SetBinContent(4, 2.86 * 86.511/397)
xs.SetBinContent(5, 1.14 * 86.511/397)
xs.SetBinContent(6, 1.0 * 86.511/397)

xsTimesEff_rinv0p1.SetBinContent(1, 1.81)
xsTimesEff_rinv0p1.SetBinContent(2, 0.18)
xsTimesEff_rinv0p1.SetBinContent(3, 0.11)
xsTimesEff_rinv0p1.SetBinContent(4, 0.12)
xsTimesEff_rinv0p1.SetBinContent(5, 0.19)
xsTimesEff_rinv0p1.SetBinContent(6, 0.65)

xsTimesEff_rinv0p5.SetBinContent(1, 1.89)
xsTimesEff_rinv0p5.SetBinContent(2, 0.15)
xsTimesEff_rinv0p5.SetBinContent(3, 0.09)
xsTimesEff_rinv0p5.SetBinContent(4, 0.10)
xsTimesEff_rinv0p5.SetBinContent(5, 0.15)
xsTimesEff_rinv0p5.SetBinContent(6, 0.63)

xsTimesEff_rinv0p9.SetBinContent(1, 1.57)
xsTimesEff_rinv0p9.SetBinContent(2, 0.13)
xsTimesEff_rinv0p9.SetBinContent(3, 0.08)
xsTimesEff_rinv0p9.SetBinContent(4, 0.07)
xsTimesEff_rinv0p9.SetBinContent(5, 0.14)
xsTimesEff_rinv0p9.SetBinContent(6, 0.62)

outf.cd()
xs.Write()
xsTimesEff_rinv0p1.Write()
xsTimesEff_rinv0p5.Write()
xsTimesEff_rinv0p9.Write()

outf.Close()
